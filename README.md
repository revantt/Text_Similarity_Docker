PREREQUISITES
1)Docker Compose

USAGE
1)Clone the repository by typing 'git clone https://github.com/revantt/Text_Similarity_Docker.git'
2)type 'sudo docker-compose build' in the directory containing the docker-compose.yml file
3)After the build is successful, type 'sudo docker-compose up' to deploy the container [The container is deployed at 0.0.0.0:5000]
4)You can now test the API through postman

STRUCTURE
1)User registers and is given 6 tokens initially
2)Everytime he uses the 'detect' API, 1 token is consumed and once he is out of tokens, he has to refill the tokens to continue using the api
3)For refill a user uses the 'refill' API in which he states the number of tokens to add to the existing tokens 

API
1)localhost:5000/register --> To register a new user use the JSON format {"username":,"password"} 
2)localhost:5000/detect --> To get the similarity between 2 texts, use the JSON format {"username":,"password":,"text1":,"text2":}
3)localhost:5000/refill --> To refill the amount of tokens given to a user, use the JSON format {"username":,"password":,"refill"}
