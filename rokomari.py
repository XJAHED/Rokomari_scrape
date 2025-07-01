from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import csv

csv_file = open('Rokomari.csv', 'w', newline='', encoding='utf-8-sig')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Author Name','Book Name','Book Price','Book Rating','Book Description','All Comments'])

# Use headless
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--disable-features=TranslateUI,VoiceInteraction")


driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

action = ActionChains(driver)
driver.get("https://www.rokomari.com/book")
action = ActionChains(driver)

author = driver.find_element(By.XPATH, '//*[@id="ts--desktop-menu"]/div[2]/div/div[1]')
action.move_to_element(author).click().perform()

# find all author
pagination = driver.find_elements(By.CSS_SELECTOR,'#author-list > div:nth-child(4) > section > div.text-center > div > a')


for p in range(1,len(pagination)):
    i = str(p)
    total_author_page = driver.find_element(By.XPATH,'//*[@id="author-list"]/div[3]/section/div[3]/div/a['+i+']').text

#####pagination
for pagi in range(1,int(total_author_page)+1):
    pa = str(pagi)
    driver.get(f'https://www.rokomari.com/book/authors?ref=sm_p0&page={pa}')
    print(f"page number is {pa}")
    
# scroll
    height = driver.execute_script('return document.body.scrollHeight')
    for s in range(0,height-2000,800):
        driver.execute_script(f'window.scrollTo(0,{s});')
        time.sleep(0.5)
    time.sleep(1)
    
    
    author = driver.find_elements(By.CSS_SELECTOR,'#author-list > div:nth-child(4) > section > div.all-authors-container > div')
    for a in range(1,len(author)+1):
        i = str(a)
        
# book click
        author_click = driver.find_element(By.CSS_SELECTOR,'#author-list > div:nth-child(4) > section > div.all-authors-container > div:nth-child('+i+') > a > h2')
        action.move_to_element(author_click).click().perform()
####author name
        try:
            author_name = driver.find_element(By.CSS_SELECTOR,'body > div.browse-page > div > div > div > section.browse__meta.author > div > div.browse__meta--author-description > h4').text
        except:
            author_name = driver.find_element(By.CSS_SELECTOR,'body > div.browse-page > div > div > div > section.browse__content > div.browse__content--heading > div > div > h1').text
        print("author name:",a,":",author_name)


####click book section
        try:
            book_pagination = driver.find_elements(By.CSS_SELECTOR,'body > div.browse-page > div > div > div > section.browse__content > div.pagination > a')
            total_pages = len(book_pagination)
            if total_pages == 0:
                total_pages = 1
        except:
            total_pages = 1
            
        for s in range(1,total_pages+1):
            driver.get(f"{driver.current_url.split('?')[0]}?page={s}")
            print("Book pagination: ", len(book_pagination))
            time.sleep(2)
            

            height = driver.execute_script('return document.body.scrollHeight')
            for s in range(0,height-2000,800):
                driver.execute_script(f'window.scrollTo(0,{s});')
                time.sleep(0.5)
            time.sleep(1)
            
            total_book_count = driver.find_elements(By.CLASS_NAME,'books-wrapper__item')
            
            for b in range(1,len(total_book_count)+1):
                time.sleep(1)
                c = str(b)
                book_click = driver.find_element(By.CSS_SELECTOR,'body > div.browse-page > div > div > div > section.browse__content > div.browse__content-books-wrapper > div > div:nth-child('+c+')')
                action.move_to_element(book_click).click().perform()
                time.sleep(2)

                # new window open and close
                main_window = driver.current_window_handle
                windows = driver.window_handles
                for window in windows:
                    if window != main_window:
                        driver.switch_to.window(window)
                        break

######Book name,price,review,comment section
                try:
                    # name
                    try:
                        book_name = driver.find_element(By.CLASS_NAME,'bookTitle_bookName__B4CEH').text
                    except:
                        book_name = "Book name not found"
                    # price
                    try:
                        book_price = driver.find_element(By.CLASS_NAME,'sell-price').text
                    except:
                        book_price = "৳"
                        
                    #### scroll
                    height = driver.execute_script('return document.body.scrollHeight')
                    for s in range(0,height-600,500):
                        driver.execute_script(f'window.scrollTo(0,{s});')
                        time.sleep(0.5)
                    #rating
                    try:
                        book_rating = driver.find_element(By.CSS_SELECTOR,'#rokomariBody > div.container > div:nth-child(6) > div:nth-child(1) > div > div.detailsReviewHeader_ratingContainer__RsQEw > div > div.detailsReviewHeader_ratingSummary___aFy_ > h3').text
                        book_ratings = f"{book_rating} ⭐"
                    except:
                        book_rating = driver.find_element(By.CSS_SELECTOR,'#rokomariBody > div.container > div:nth-child(7) > div:nth-child(1) > div > div.detailsReviewHeader_ratingContainer__RsQEw > div > div.detailsReviewHeader_ratingSummary___aFy_ > h3').text
                        book_ratings = f"{book_rating} ⭐"
                    #description
                    try:
                        book_description = driver.find_element(By.CLASS_NAME,'productSummary_summeryText__Pd_tX').text
                    except:
                        book_description = "No summary"
                    time.sleep(2)
                    

                    #comment
                    for i in range(1,40):
                        try:
                            try:
                                show_more_btn = driver.find_element(By.CSS_SELECTOR, '#rokomariBody > div.container > div:nth-child(6) > div.cardContainer_frontProductList__TP9Eo.cardContainer_reviewSectionContainer__TmIwS > div > div > div > div > button')
                            except:
                                show_more_btn = driver.find_element(By.CSS_SELECTOR, '#rokomariBody > div.container > div:nth-child(7) > div.cardContainer_frontProductList__TP9Eo.cardContainer_reviewSectionContainer__TmIwS > div > div > div > div > button')
                            action.move_to_element(show_more_btn).click().perform()
                            time.sleep(0.5)
                        except:
                            break

                    try:
                        all_comments = driver.find_elements(By.CLASS_NAME, 'singleReview_reviewComment__gKQY8')
                        comment_texts = []
                        for comments in all_comments:
                            all_cmt = comments.text.strip()
                            if all_cmt:
                                comment_texts.append(all_cmt)
                            else:
                                 comment_texts.append("No comment")
                            all_cmt_joined = " |    | ".join(comment_texts)
                        time.sleep(5)
                    except:
                        all_cmt_joined = "No comments"
    
                except:
                    print("book not found")
    
                finally:
                    try:
                        driver.close()
                        driver.switch_to.window(main_window)
                    except Exception as e:
                        print("Window switching issue:", e)
                        break
    
                csv_writer.writerow([author_name, book_name, book_price, book_ratings, book_description, all_cmt_joined])

####back page number
        driver.get(f'https://www.rokomari.com/book/authors?ref=sm_p0&page={pa}')
        
time.sleep(10)
