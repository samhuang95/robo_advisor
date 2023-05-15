from connect_to_db import SQLcommand
from datetime import datetime
import requests, os

def get_insights(data: dict) -> list:
  insights_dict = {insights_data['name']: insights_data['values'][0]['value'] for insights_data in data}

  insights_dict['post_impressions_by_story_type'] = insights_dict['post_impressions_by_story_type']['other'] if 'other' in insights_dict['post_impressions_by_story_type'] else 0
  insights_dict['post_impressions_by_story_type_unique'] = insights_dict['post_impressions_by_story_type_unique']['other'] if 'other' in insights_dict['post_impressions_by_story_type_unique'] else 0
  
  insights_dict['post_negative_feedback_by_type_hide_all_clicks'] = insights_dict['post_negative_feedback_by_type']['hide_all_clicks'] if 'hide_all_clicks' in insights_dict['post_negative_feedback_by_type'] else 0
  insights_dict['post_negative_feedback_by_type_hide_clicks'] = insights_dict['post_negative_feedback_by_type']['hide_clicks'] if 'hide_clicks' in insights_dict['post_negative_feedback_by_type'] else 0
  insights_dict['post_negative_feedback_by_type_unique_hide_all_clicks'] = insights_dict['post_negative_feedback_by_type_unique']['hide_all_clicks'] if 'hide_all_clicks' in insights_dict['post_negative_feedback_by_type_unique'] else 0
  insights_dict['post_negative_feedback_by_type_unique_hide_clicks'] = insights_dict['post_negative_feedback_by_type_unique']['hide_clicks'] if 'hide_clicks' in insights_dict['post_negative_feedback_by_type_unique'] else 0

  insights_dict['post_clicks_by_type_other_clicks'] = insights_dict['post_clicks_by_type']['other clicks'] if 'other clicks' in insights_dict['post_clicks_by_type'] else 0
  insights_dict['post_clicks_by_type_photo_view'] = insights_dict['post_clicks_by_type']['photo view'] if 'photo view' in insights_dict['post_clicks_by_type'] else 0
  insights_dict['post_clicks_by_type_link_clicks'] = insights_dict['post_clicks_by_type']['link clicks'] if 'link clicks' in insights_dict['post_clicks_by_type'] else 0
  insights_dict['post_clicks_by_type_unique_other_clicks'] = insights_dict['post_clicks_by_type_unique']['other clicks'] if 'other clicks' in insights_dict['post_clicks_by_type_unique'] else 0
  insights_dict['post_clicks_by_type_unique_photo_view'] = insights_dict['post_clicks_by_type_unique']['photo view'] if 'photo view' in insights_dict['post_clicks_by_type_unique'] else 0
  insights_dict['post_clicks_by_type_unique_link_clicks'] = insights_dict['post_clicks_by_type_unique']['link clicks'] if 'link clicks' in insights_dict['post_clicks_by_type_unique'] else 0

  insights_dict['post_reactions_by_type_total_like'] = insights_dict['post_reactions_by_type_total']['like'] if 'like' in insights_dict['post_reactions_by_type_total'] else 0
  insights_dict['post_reactions_by_type_total_love'] = insights_dict['post_reactions_by_type_total']['love'] if 'love' in insights_dict['post_reactions_by_type_total'] else 0
  insights_dict['post_reactions_by_type_total_wow'] = insights_dict['post_reactions_by_type_total']['wow'] if 'wow' in insights_dict['post_reactions_by_type_total'] else 0
  insights_dict['post_reactions_by_type_total_haha'] = insights_dict['post_reactions_by_type_total']['haha'] if 'haha' in insights_dict['post_reactions_by_type_total'] else 0
  insights_dict['post_reactions_by_type_total_sorry'] = insights_dict['post_reactions_by_type_total']['sorry'] if 'sorry' in insights_dict['post_reactions_by_type_total'] else 0
  insights_dict['post_reactions_by_type_total_anger'] = insights_dict['post_reactions_by_type_total']['anger'] if 'anger' in insights_dict['post_reactions_by_type_total'] else 0
  
  del insights_dict['post_impressions_by_story_type']
  del insights_dict['post_impressions_by_story_type_unique']
  del insights_dict['post_negative_feedback_by_type']
  del insights_dict['post_negative_feedback_by_type_unique']
  del insights_dict['post_clicks_by_type']
  del insights_dict['post_clicks_by_type_unique']
  del insights_dict['post_reactions_by_type_total']
  
  return list(insights_dict.values())

def get_post_data(fanpage_access_token: str) -> None:
  fields = 'posts.limit(50){id,created_time,is_popular,message,message_tags,shares{count},attachments{media{image{src}},subattachments{media{image{src}}}},comments.summary(total_count),insights.metric(post_impressions,post_impressions_unique,post_impressions_fan,post_impressions_fan_unique,post_impressions_viral,post_impressions_viral_unique,post_impressions_nonviral,post_impressions_nonviral_unique,post_impressions_by_story_type,post_impressions_by_story_type_unique,post_engaged_users,post_negative_feedback,post_negative_feedback_unique,post_negative_feedback_by_type,post_negative_feedback_by_type_unique,post_engaged_fan,post_clicks,post_clicks_unique,post_clicks_by_type,post_clicks_by_type_unique,post_reactions_by_type_total),likes.summary(total_count),reactions.summary(total_count)}'
  url = f'https://graph.facebook.com/548711105217630?fields={fields}&access_token={fanpage_access_token}'

  response = requests.get(url)
  data = response.json()['posts'] if 'posts' in response.json() else response.json()

  for post_data in data['data']:
    post_id = post_data['id'].split('_')[1]
    if SQLcommand().get(f'SELECT id FROM facebook_posts WHERE id = {post_id}'): continue

    post_time = post_data['created_time'].replace('T', ' ').split('+')[0]
    if (datetime.utcnow() - datetime.strptime(post_time, '%Y-%m-%d %H:%M:%S')).days < 7: continue

    post_text = post_data['message'] if 'message' in post_data else ''
    post_likes = post_data['likes']['summary']['total_count']
    post_reactions = post_data['reactions']['summary']['total_count']
    post_shares = post_data['shares']['count'] if 'shares' in post_data else 0
    post_comments = post_data['comments']['summary']['total_count']
    post_popular = post_data['is_popular']
    
    values_string = str(tuple([post_id, post_time, post_text, post_likes, post_reactions, post_shares, post_comments, post_popular] + get_insights(post_data['insights']['data'])))
    SQLcommand().modify(f'INSERT INTO facebook_posts (id, time, text, likes, reactions, shares, comments, popular, post_impressions, post_impressions_unique, post_impressions_fan, post_impressions_fan_unique, post_impressions_viral, post_impressions_viral_unique, post_impressions_nonviral, post_impressions_nonviral_unique, post_engaged_users, post_negative_feedback, post_negative_feedback_unique, post_engaged_fan, post_clicks, post_clicks_unique, post_negative_feedback_by_type_hide_all_clicks, post_negative_feedback_by_type_hide_clicks, post_negative_feedback_by_type_unique_hide_all_clicks, post_negative_feedback_by_type_unique_hide_clicks, post_clicks_by_type_other_clicks, post_clicks_by_type_photo_view, post_clicks_by_type_link_clicks, post_clicks_by_type_unique_other_clicks, post_clicks_by_type_unique_photo_view, post_clicks_by_type_unique_link_clicks, post_reactions_by_type_total_like, post_reactions_by_type_total_love, post_reactions_by_type_total_wow, post_reactions_by_type_total_haha, post_reactions_by_type_total_sorry, post_reactions_by_type_total_anger) VALUES {values_string}')


if __name__ == '__main__':
  fanpage_access_token = os.getenv('FANPAGE_ACCESS_TOKEN')
  get_post_data(fanpage_access_token)
  print('已完成資料庫更新！')
