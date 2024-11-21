import paho.mqtt.client as mqtt 
import time
import requests

broker_hostname = "localhost"
port = 1883 

def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("connected")
    else:
        print("could not connect, return code:", return_code)

def yelp_to_pubsub():
    # Define your Yelp Fusion API credentials
    client_id = '3C8py-b3W606H54OVHgH4g'
    api_key = 'ylZ9TmcoAy_kc7kWfSgKak07GzJf4ks0Dvys-hU4tT71N6-_leVAkkmPIXwJ8bon91dW00iCjwWhXpqdA7DyTRAGb3La2D46Vz3qph4yFmuilsfxGmMT8M1hpOU5ZXYx'

    # Define your search parameters
    search_params = {
        'term': 'Pizza',
        'location': 'New York, NY',
        'limit': 30  # You can adjust the number of results per request
    }

    # Define the base URL for Yelp Fusion API
    base_url = 'https://api.yelp.com/v3/businesses/search'

    # Set up the headers with your API Key
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    yelp_reviews = []

    # Make the initial request to Yelp Fusion API
    response = requests.get(base_url, headers=headers, params=search_params)

    if response.status_code == 200:
        data = response.json()
        businesses = data.get('businesses', [])

        for business in businesses:
            business_name = business['name']
            business_id = business['id']

            # Make a request to get reviews for the business
            reviews_url = f'https://api.yelp.com/v3/businesses/{business_id}/reviews'
            reviews_response = requests.get(reviews_url, headers=headers)

            if reviews_response.status_code == 200:
                reviews_data = reviews_response.json()
                reviews = reviews_data.get('reviews', [])

                # Calculate the average rating for the business
                ratings = [review['rating'] for review in reviews]
                average_rating = sum(ratings) / len(ratings) if ratings else 0

                yelp_reviews.append({
                    'title': business_name,
                    'average_rating': average_rating,
                    'reviews': reviews
                })

    return yelp_reviews

client = mqtt.Client()
client.username_pw_set(username="likith", password="likith") # uncomment if you use password auth
client.on_connect = on_connect

client.connect(broker_hostname, port)
client.loop_start()

topic = "Test"

try:
    # Fetch reviews from Yelp API
    reviews = yelp_to_pubsub()

    # Publish each review as a message to the MQTT topic
    for business in reviews:
        business_name = business['title']
        average_rating = business['average_rating']
        reviews = business['reviews']

        for review in reviews:
            # Construct a message with details of the review
            review_message = f"Business: {business_name}, Average Rating: {average_rating}, " \
                            f"Review Rating: {review.get('rating', 'N/A')}, Review Text: {review.get('text', 'No text provided')}"
            
            # Publish the message
            result = client.publish(topic, review_message)
            status = result[0]
            if status == 0:
                print(f"Published: {review_message}")
            else:
                print("Failed to publish message")
                if not client.is_connected():
                    print("Client not connected, exiting...")
                    break
            time.sleep(1)  # Add a delay between messages to avoid flooding the broker

finally:
    client.disconnect()
    client.loop_stop()
