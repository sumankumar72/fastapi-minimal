name: Build and Push Django Image to AWS ECR
on:
  push:
    branches:
      - cns
      - prod
      - stage
jobs:
  build:
    name: Build and Push to ECR
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v2

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1

    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1

    - name: Automatic Tagging of Releases
      id: increment-git-tag
      run: echo "sha_short=$(git rev-parse --short HEAD)" >> $GITHUB_OUTPUT

    - name: Build, Tag, and Push the Image to Amazon ECR
      id: build-image
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        ECR_REPOSITORY: spc-backend
        IMAGE_TAG: ${{ steps.increment-git-tag.outputs.sha_short }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
    
    - name: Cleanup old images in ECR
      env:
        AWS_REGION: us-east-1
        ECR_REPOSITORY: spc-backend
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
      run: |
          # Fetch and sort the image tags by the push time in descending order
          image_tags=$(aws ecr describe-images --repository-name $ECR_REPOSITORY --query 'imageDetails | sort_by(@, &imagePushedAt) | reverse(@)[].imageTags[0]' --output text --region $AWS_REGION)
          
          # Convert to array
          tags_array=($image_tags)

          # Get the length of the array
          tags_count=${#tags_array[@]}

          # Ensure there are more than 2 images to delete
          if [ $tags_count -le 2 ]; then
            echo "There are $tags_count images in the repository. No cleanup needed."
            exit 0
          fi

          # Remove the two most recent tags from the array
          tags_to_delete=("${tags_array[@]:2}")

          for tag in "${tags_to_delete[@]}"; do
            if [ -n "$tag" ]; then
              echo ""
              echo ""
              echo ""
              echo "******************* START *********************"
              echo "Deleting image: $ECR_REGISTRY/$ECR_REPOSITORY:$tag"
              aws ecr batch-delete-image --repository-name $ECR_REPOSITORY --image-ids imageTag=$tag --region $AWS_REGION
              echo "******************* END *********************"
            fi
          done
      
  deploy:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Checkout
        uses: actions/checkout@v2
      
      - name: Set environment for branch
        run: |
          if [[ $GITHUB_REF_NAME == 'prod' ]]; then
            echo "DB_NAME=stspc" >> "$GITHUB_ENV"
            echo "EC2_HOST=stpc.satet.us" >> "$GITHUB_ENV"
          else
            if [[ $GITHUB_REF_NAME == 'cns' ]]; then
              echo "DB_NAME=cns_db" >> "$GITHUB_ENV"
              echo "EC2_HOST=cns.satet.us" >> "$GITHUB_ENV"
            else
              echo "DB_NAME=stpc_stage" >> "$GITHUB_ENV"
              echo "EC2_HOST=stpc.satet.us" >> "$GITHUB_ENV"
            fi
          fi

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1

      - name: Automatic Tagging of Releases
        id: increment-git-tag
        run: echo "sha_short=$(git rev-parse --short HEAD)" >> $GITHUB_OUTPUT

      - name: SSH into EC2
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: spc-backend
          IMAGE_TAG: ${{ steps.increment-git-tag.outputs.sha_short }}
        uses: appleboy/ssh-action@master
        with:
          host: ${{ env.EC2_HOST }}
          username: ${{ vars.EC2_USERNAME }}
          key: ${{ secrets.EC2_PRIVATE_KEY }}
          script: |
            aws configure set aws_access_key_id ${{ secrets.AWS_ACCESS_KEY_ID }}
            aws configure set aws_secret_access_key ${{ secrets.AWS_SECRET_ACCESS_KEY }}
            aws configure set default.region us-east-1

            aws ecr get-login-password --region us-east-1 | sudo docker login --username AWS --password-stdin ${{ steps.login-ecr.outputs.registry }}
  
            export ECR_REGISTRY=${{ steps.login-ecr.outputs.registry }}
            export ECR_REPOSITORY=spc-backend
            export IMAGE_TAG=${{ steps.increment-git-tag.outputs.sha_short }}
            export DB_NAME=${{ env.DB_NAME }}
            export DB_USER=${{ secrets.DB_USER }}
            export DB_PASSWORD=${{ secrets.DB_PASSWORD }}

            cat <<EOF > docker-compose.yml
            version: '3'
            services:
              spc-backend:
                image: ${{ steps.login-ecr.outputs.registry }}/spc-backend:${{ steps.increment-git-tag.outputs.sha_short }}
                ports:
                  - "8000:8000"
                volumes:
                - /home/ubuntu/static_stage:/app/static
                environment:
                  DB_NAME: ${{ env.DB_NAME }}
                  DB_USER: ${{ secrets.DB_USER }}
                  DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
            EOF

            sudo docker-compose pull spc-backend
            sudo docker-compose up -d --no-deps spc-backend

            sudo docker image prune -a -f