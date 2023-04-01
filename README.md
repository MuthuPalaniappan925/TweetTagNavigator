
# Tweet-Tag-Navigator

The Tweet Tag Navigator repository is a project that utilizes deep learning techniques to assign multi-class labels to tweets based on their content. The repository contains code that uses state-of-the-art natural language processing (NLP) model BERT - ZERO SHOT LEARNING to analyze the text of tweets and predict which topics or themes they are related to.

# Goal of the Project
Help users quickly navigate through large volumes of tweets by providing them with relevant tags that summarize the content of each tweet. This can be useful in a variety of applications, such as social media monitoring, trend analysis, and sentiment analysis.

# Output
The output of the model is a set of probabilities that indicate the likelihood of the tweet belonging to each label. These probabilities can be used to rank the tags in order of relevance or to filter tweets based on their predicted labels.

## API Reference

### Twitter API V2

```http
  statuses/user_timeline
```
#### Returns a collection of the most recent Tweets posted by the specified user.


```http
  search/tweets
```
#### Returns a collection of relevant Tweets matching a specified query.

```http
  statuses/show/:id
```
#### Returns a single Tweet, specified by the id parameter.

## Authentication

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `consumer_key` | `string` | **Required**. Your API key |
| `consumer_secret` | `string` | **Required**. Your API Secret Token |
| `access_token` | `string` | **Required**. Your Access Token |
| `access_token_secret` | `string` | **Required**. Your Access Secret Token |

#### 

```http
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token,  access_token_secret)
```


## Requirments

``` http
pip install -r requirments.txt
```

## Installation and Running

- Clone the repository to your local machine using the command ``` git clone https://github.com/MuthuPalaniappan925/TweetTagNavigator.git```
- Navigate to the project directory using the command ```cd TweetTagNavigator```.
- Install the required dependencies using the command ```pip install -r requirements.txt```.
- Run the command ```flask run``` to start the server.
- Open your web browser and navigate to ```http://localhost:5000``` to view the application.

## Future Work
Deployment using a web server like Apache or Nginx to serve the Flask application.
