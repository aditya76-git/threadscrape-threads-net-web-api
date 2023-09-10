import json
from .errors import ThreadScrapeError

def get_json_response(response, error_message, expected_status_codes = [200]):
    """
    Handle common tasks for JSON responses, including checking status codes.

    Args:
        response (requests.Response): The HTTP response object.
        error_message (str): Custom error message to raise in case of errors.
        expected_status_codes (list): List of expected HTTP status codes.

    Returns:
        dict: Parsed JSON response.

    Raises:
        ThreadScrapeError: If the response status code is not in the expected list or if there are GraphQL errors.
    """

    if response.status_code not in expected_status_codes:
        raise ThreadScrapeError(error_message)

    try:
        response_json = response.json()
        if 'errors' in response_json:
            # Handle GraphQL errors
            error_messages = [error.get('message', 'Unknown error') for error in response_json['errors']]
            raise ThreadScrapeError('\n'.join(error_messages))
        return response_json
    
    except json.JSONDecodeError:
        raise ThreadScrapeError("Error decoding JSON response")




def arrange_media_data(json_data, image_size="original"):

    data = json_data

    carousel_media = data['data']['data']['edges'][0]['node']['thread_items'][0]['post']['carousel_media']

    # Initialize an empty list to store image URLs
    images = []
    videos = []
    if carousel_media is not None:
      # Iterate through carousel media and append image URLs with the specified size to the list
      for index, media in enumerate(carousel_media):
          image_versions = media.get('image_versions2', {})
          if image_versions:
              for candidate in image_versions.get('candidates', []):
                  url = candidate.get('url', '')
                  if image_size == "original" or f"_s{image_size}x{image_size}" in url:
                      image_data = {
                          "url": url,
                          "height": image_size if image_size != "original" else media.get("original_height", ""),
                          "width": image_size if image_size != "original" else media.get("original_width", ""),
                          "index": index + 1  # Add the index to image_data
                      }
                      images.append(image_data)
                      break  # Stop looking for other sizes once found


    else:
          image_versions = data['data']['data']['edges'][0]['node']['thread_items'][0]['post']
      
          image_data = {
              "url": image_versions.get('image_versions2', [{}]).get('candidates', [{}])[0].get('url'),
              "height": image_versions.get("original_height", ""),
              "width": image_versions.get("original_width", ""),
              "index": 1  # Add the index for the fallback image
          }
          images.append(image_data)

    result = {
        "images": images,
        "videos": videos
    }

    return result