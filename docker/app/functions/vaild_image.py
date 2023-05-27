import requests
from image_predict import predict_image
from urllib.request import urlretrieve
from clear_folder import clear_folder
from datetime import datetime

fanpage_access_token = 'EAADNZCmChXTsBABWVSxjCzk6KE9Frb9Ho0GjNSXC3blc54dTB3HNyVHpf7eWoGle1ZCxozufEVkQHiGtEZBZAe0YKPhykJGMZCKNAS22w1u4xmoYZCAZCTTgi3TZAcSWyoZAncJ4BUmZCim1LZANOjJriDOLtE0it35CZALTKTZCgzMgACGBHTSZAqaSQf'
fields = 'posts.limit(50){id,created_time,attachments{media{image{src}},subattachments{media{image{src}}}},insights.metric(post_impressions_unique,post_clicks_by_type)}'
url = f'https://graph.facebook.com/548711105217630?fields={fields}&access_token={fanpage_access_token}'

def validate_image(start_date, end_date):
  clear_folder('/app/functions/photos/')

  start_date = datetime.strptime(start_date, '%Y-%m-%d')
  end_date = datetime.strptime(end_date, '%Y-%m-%d')

  data = requests.get(url).json()['posts']
  for post_data in data['data']:
    post_time = datetime.strptime(post_data['created_time'].replace('T', ' ').split('+')[0], '%Y-%m-%d %H:%M:%S')
    if post_time < start_date or post_time > end_date: continue

    post_id = post_data['id'].split('_')[1]
    post_impressions = post_data['insights']['data'][0]['values'][0]['value']
    photo_views = post_data['insights']['data'][1]['values'][0]['value'].get('photo view')

    if photo_views / post_impressions < 0.0039728349886637305: score = 'C'
    elif photo_views / post_impressions < 0.015248001220329647: score = 'B'
    elif photo_views / post_impressions < 0.045274756321514335: score = 'A'
    else: score = 'S'

    i = 1
    if 'attachments' in post_data:
      photo_url = post_data['attachments']['data'][0]['media']['image']['src']
      if 'external' not in photo_url:
        urlretrieve(photo_url, f'/app/functions/photos/{post_id}_{i}.jpg')
        predict_score = predict_image(f'/app/functions/photos/{post_id}_{i}.jpg')
        with open ('/app/functions/result.txt', 'a') as file:
          file.write(f'{post_id}_{i} {score} {predict_score}\n')
        i += 1
      if 'subattachments' in post_data['attachments']['data'][0]:
        for photo in post_data['attachments']['data'][0]['subattachments']['data'][1:]:
          photo_url = photo['media']['image']['src']
          if 'external' not in photo_url:
            urlretrieve(photo_url, f'/app/functions/photos/{post_id}_{i}.jpg')
            predict_score = predict_image(f'/app/functions/photos/{post_id}_{i}.jpg')
            with open ('/app/functions/result.txt', 'a') as file:
              file.write(f'{post_id}_{i} {score} {predict_score}\n')
            i += 1

if __name__ == '__main__':
  validate_image('2023-05-01', '2023-05-15')