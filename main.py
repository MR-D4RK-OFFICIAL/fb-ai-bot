import os
import time
import requests
import google.generativeai as genai
from bs4 import BeautifulSoup

# কনফিগারেশন
API_KEY = "AIzaSyCbiHTpp9xpP_s2VoFyMsI2tsYQRlSl1e0"
COOKIE = "datr=KtPYab6AG9gB9spXf1EuaUKI;sb=KtPYafmr1nifAzXVk_hna5DT;dpr=3.2983407974243164;ps_l=1;ps_n=1;wd=891x1802;c_user=61550785142416;fr=1eDEuZOpX4e7aNR3F.AWcu01o3peTP7Hl-xUxwM1iYIHO1DyJuE8rk53t_EoQiRyusQ_U.Bp341J..AAA.0.0.Bp341J.AWc02rikP6etBgvmVm5r4Vg5JYg;xs=8%3ADq8jU-LYMze95g%3A2%3A1776258369%3A-1%3A-1%3A%3AAczBPNDcXQlcPQ5GifUPEe69kv34avf3E0Lw87pq2g;"

# Gemini AI সেটআপ
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_ai_comment(post_text):
    try:
        prompt = f"Write a short, friendly, one-line Bengali comment for this FB post: {post_text}. Don't use emojis."
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "Nice post!"

def start_bot():
    headers = {
        'cookie': COOKIE,
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
    }
    
    print("Bot started...")
    
    while True:
        try:
            # ফেসবুক নিউজফিড লোড করা
            response = requests.get("https://mbasic.facebook.com/", headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # পোস্ট খুঁজে বের করা
            posts = soup.find_all('div', role='article')
            
            for post in posts:
                # পোস্টের টেক্সট নেওয়া
                post_text = post.get_text()
                
                # কমেন্ট বক্সের লিংক খোঁজা
                comment_link = post.find('a', string=lambda x: x and 'Comment' in x)
                
                if comment_link:
                    link = "https://mbasic.facebook.com" + comment_link['href']
                    
                    # AI থেকে কমেন্ট তৈরি
                    comment = get_ai_comment(post_text)
                    
                    # কমেন্ট সাবমিট করার লজিক (সংক্ষেপে)
                    # দ্রষ্টব্য: এখানে সাবমিট করার জন্য আরও একটি রিকোয়েস্ট লাগবে
                    print(f"Post found: {post_text[:30]}...")
                    print(f"AI Suggestion: {comment}")
                    
            # ৫ মিনিট বিরতি যাতে আইডি ব্লক না হয়
            time.sleep(300) 
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    start_bot()
