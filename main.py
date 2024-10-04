from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
import json
import os
from firebase import firebase
import openai
from datetime import datetime, timedelta

# 使用環境變量讀取憑證
openai.api_key = os.getenv('OPENAI_API_KEY')
token = os.getenv('LINE_BOT_TOKEN')
secret = os.getenv('LINE_BOT_SECRET')
firebase_url = os.getenv('FIREBASE_URL')

def linebot(request):
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    try:
        line_bot_api = LineBotApi(token)
        handler = WebhookHandler(secret)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        event = json_data['events'][0]
        tk = event['replyToken']
        user_id = event['source']['userId']
        msg_type = event['message']['type']

        fdb = firebase.FirebaseApplication(firebase_url, None)
        user_chat_path = f'chat/{user_id}'
        chat_state_path = f'state/{user_id}'
        chatgpt = fdb.get(user_chat_path, None)

        current_time = datetime.now()
        last_interaction_time = fdb.get(chat_state_path, 'last_interaction')

        if last_interaction_time:
            # 將上次消息的時間戳轉換為 datetime 對象
            last_interaction_time = datetime.strptime(last_interaction_time, '%Y-%m-%d %H:%M:%S.%f')
            print(last_interaction_time)
            print(current_time)
            print(current_time-last_interaction_time)
            print(current_time - last_interaction_time > timedelta(hours=12))
            # 檢查時間間隔是否超過24小時
            if current_time - last_interaction_time > timedelta(hours=24):
                # 如果超過24小時，清空對話記錄
                chatgpt = None
                fdb.delete(user_chat_path, None)

        if msg_type == 'text':
            msg = event['message']['text']

            if chatgpt is None:
                messages = [
                    {"role": "user", "content": "Prelude X 系列設計輕薄短小，隨身攜帶無負擔。Prelude X 行動電源（5000 mAh)：102x62x12.7mm，151g，額定容量3000mAh;Prelude XR 行動電源（10000mAh）：102x62x19 mm，225g，額定容量6000mAh;Prelude XS 充電插頭 （27Ｗ快充）：21x58 mm，80g"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude  X 系列行動電源MagSafe具備快充，傳輸過程中會有能量損耗，進而產生一定的熱量，出現發熱的現象，屬正常情況。Prelude X 系列皆有通過多國電子裝置安全認證，可以安心使用，同時搭載過熱自動斷電的機制，並保護電池的健康度！"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude  X 系列行動電源在電流轉換過程時會發出的微聲，屬正常現象，並非產品故障，可放心使用"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude  X 系列行動電源底部提供電量顯示，由紅色與藍色區分目前電量%數，如電量指示燈紅燈快速閃爍，表示低電量，需要為Prelude X/XR充電。紅燈閃爍為0%-30%藍燈閃爍 30%-99%藍燈為100%"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude X 系列行動電源依照 Apple 官方提供的 MagSafe 規格尺寸打造，凡 iPhone 12 以上機型不會卡鏡頭哦！"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "遇到對方說行動電源故障或是車充故障，你要回:您好，商品我們有提供維修和檢測服務，麻煩您提供訂購日期、訂購編號、訂購電話，請稍候，客服專員將會協助您處理。客服服務時間為週一至週五，8:30am～17:30pm。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "遇到對方說行動電源破裂或是車充破裂，你要回:您好，商品我們有提供維修和檢測服務，麻煩您提供訂購日期、訂購編號、訂購電話，請稍候，客服專員將會協助您處理。客服服務時間為週一至週五，8:30am～17:30pm。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "遇到對方說行動電源支架斷裂或是車充支架斷掉，你要回:您好，商品我們有提供維修和檢測服務，麻煩您提供訂購日期、訂購編號、訂購電話，請稍候，客服專員將會協助您處理。客服服務時間為週一至週五，8:30am～17:30pm。"},
                    {"role": "assistant", "content": "記住了!"},                         
                    {"role": "user", "content": "遇到對方說行動電源無法充電，你要回:您好，商品我們有提供維修和檢測服務，麻煩您提供訂購日期、訂購編號、訂購電話，請稍候，客服專員將會協助您處理。客服服務時間為週一至週五，8:30am～17:30pm。"},
                    {"role": "assistant", "content": "記住了!"}, 
                    {"role": "user", "content": "遇到對方查詢訂單，你要回:您好，請提供訂單以下資訊:訂單編號、訂購平台、訂購姓名、訂購電話。請稍候客服專員會盡快回覆您客服服務時間：週一～週五 8:30am～17:30pm"},
                    {"role": "assistant", "content": "記住了!"}, 
                    {"role": "user", "content": "Prelude X系列行動電源保固是18個月，登入保固資料可延長保固至24個月;Omnia X車充保固是12個月，登入保固資料可延長保固至18個月"},
                    {"role": "assistant", "content": "記住了!"},       
                    {"role": "user", "content": "延長保固步驟:先加入官方Line ID：@667jjfhr→ 點選『主選單』登入保固→ 填寫線上保固資料 → 填寫完成，回到LINE上回覆「已填寫保固申請表」"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "遇到對方說已登記完保固資訊，你要回:謝謝您登記保固資訊，祝您有美好的充電體驗。"},
                    {"role": "assistant", "content": "記住了!"},        
                    {"role": "user", "content": "聯絡資訊:客服電話：（05）224-2828 服務時間：週一至週五，09：00~12：30 ／13：30~17：00"},
                    {"role": "assistant", "content": "記住了!"}, 
                    {"role": "user", "content": "遇到對方說我要退貨，你要回:▲如需退貨，產品上保護膜請勿撕掉。請稍候客服專員會盡快回覆您，客服服務時間：週一～週五 8：30am～17：30pm"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "遇到對方詢問退貨，你要回:官網消費的消費者，都可以依照消費保護法規定，享有七天猶豫期的權利。但猶豫期並非試用期，您退回的商品需要是全新的狀態、完整包裝。請注意保持商品本體、配件、贈品、說明書、原廠包裝及所有文件的完整性，切勿缺漏任何配件或損毀原廠外盒，如有缺漏將會影響您退換貨的權益。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "遇到對方說行動電源膨脹，你要回:您好，行動電源如有膨脹現象請勿繼續使用，麻煩您提供訂購日期、訂購編號、訂購電話，請稍候，客服專員將會協助您處理。客服服務時間為週一至週五，8:30am～17:30pm。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude XS設計為 A型插頭，電壓110-240V皆可使用，可依據國家需求搭配轉接頭與變壓器一起使用。"},
                    {"role": "assistant", "content": "記住了!"}, 
                    {"role": "user", "content": "Omnia X車充規格:USB-C輸入：5V/3A,9V/3A，無線輸出1：5W/7.5W/10W/15W，無線輸出2：5W，無線輸出3：5W，球頭為17mm公規。"},
                    {"role": "assistant", "content": "記住了!"}, 
                    {"role": "user", "content": "Omnia X車充專為 iPhone MagSafe 裝置設計，只要是有支援 MagSafe 的手機殼或是裸機皆可使用。＊iPhone 12 以上皆有支援 MagSafe，Android 手機若有加裝引磁貼片也可使用磁吸無線充電，建議引磁貼片應當精確對準磁吸線圈，避免影響充電效率。"},
                    {"role": "assistant", "content": "記住了!"}, 
                    {"role": "user", "content": "Omnia X 車充磁吸力優於Apple 官方標準磁吸力 1.2 KG，經半年以上實測，手機直式橫式自由切換都能緊密吸附，安全穩固。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "實體展售店舖資訊：https://reurl.cc/yvLnx8"},
                    {"role": "assistant", "content": "記住了!"}, 
                    {"role": "user", "content": "Omnia X車充材質為ABS，內部則為金屬，最大承重可達5KG不鬆脫"},
                    {"role": "assistant", "content": "記住了!"},  
                    {"role": "user", "content": "BMW IX車系為曲面螢幕，會建議使用吸盤式支架搭配Omnia X車充在A柱玻璃上。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Omnia X車充總共提供三種支架選擇！任何車型都適用。分別是:智慧型轉軸式勾夾支架：適用橫式冷氣風扇，方便使用、穩定度高;吸盤式車用支架（須加購）：不挑車款，使用可水洗強力吸盤，吸力不減;電動車 Tesla 專用支架（須加購）：電動車 Tesla 專用，可折疊收納於螢幕後方"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "如果有消費者詢問優惠活動，你要回:很抱歉，目前沒有優惠活動，不過近期將會推出優惠活動，可以追蹤我們臉書社團掌握第一手資訊https://www.facebook.com/BEZALEL.CO?locale=zh_TW"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "行動電源與車充皆有過溫、過載、過充保護機制，並通過多國國際安全認證。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "目前 Apple 系列產品僅有 iPhone 13 以上且軟體須更新 iOS 17.2 才有支援 Qi2 15W 的無線充電，若後續 Apple 官方有將 iPhone 13 以下的型號也升級到支援 Qi2，亦可達到 15W 無線充電"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "車充內附商品有:Omnia X MagSafe 車充*1、智慧型轉軸式勾夾支架 *1、USB-C 充電線 *1、User 使用說明書 *1"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "車充充電座僅支持Apple Watch 或 Air Pods其一設備充電"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "車充不建議三明治充電，而Prelude X系列行動電源可以三明治充電，但建議XS插頭直充手機或行動電源，充電效益會較好"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "車充支架前端皆為球狀轉軸，可以 360 度自由調整角度，調整到合適的角度後可將旋鈕鎖緊，即可固定。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "《 Omnia X MagSafe 車用磁吸無線充電器 》 一次可支援兩個裝置同時充電，手機＋AirPods / AirPods Pro / Apple Watch。＊凡支援無線充電與 MagSafe 充電盒的 AirPods 皆可使用。再搭配《 85W 三孔車用快充頭 》 第二孔可為 Omnia X 提供電力，另外兩孔可以再充其他裝置！如：行車記錄器、筆電、平板等。所以一共可以一次充四個裝置!"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "特斯拉支架不穩固的解決方法:先將黏貼面黏在螢幕後面按壓黑色鎖紐把空氣完全排除（黏膠面的空氣都排出會更牢固），靜置半小時左右，讓黏膠完全貼合在螢幕後方，再開始調整支架角度或安裝車充本體，避免黏膠尚未固定下進行安裝調整，會容易造成黏膠過程鬆脫，支架部分都需鎖緊（鎖緊後可再多鎖半圈左右），確保支架不易晃動。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "黏貼過程中未穩固情況下進行安裝支架及調整角度，外力拉扯造成膠面受損捲曲變形，就像黏貼３Ｍ掛勾一個未黏緊或是剛黏好馬上放上重物會很容易掉落。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude X 系列行動電源的 MagSafe 磁吸功能 提供iPhone 12 以上的機型以及加裝 MagSafe 手機殼使用，只要搭載 MagSafe 的裝置或裸機都能夠使用。而凡是支援Qi無線充電與Android手機都能使用Prelude X系列產品進行充電和PD 20W 快充的有線充電！(使用一般手機殼的話可能會影響到磁吸力和充電效率)"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude XS 充電插頭可以180度旋轉，不會佔用插座，還能夠使用三明治充電術同時充 Prelude X/XR 行動電源與手機，還能再使用 Type-C 有線 27W 快充，一個 XS 充電插頭三個裝置同時充電"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude X 行動電源（5000 mAh）：20W 有線輸出 / Qi 15W 無線輸出 / MagSafe 7.5W 無線輸出;Prelude XR 行動電源（10000 mAh）：20W 有線輸出 / Qi 15W 無線輸出 / MagSafe 7.5W 無線輸出;Prelude XS 無線充電插頭：27W 有線輸出 / 10Ｗ 無線輸出"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude XS 充電插頭無需開關電源鍵，輕輕一靠即可充電。Prelude X/XR 行動電源，因為支援雙面充電，最多同時可充三個裝置，因此需要電源鍵來控制充電"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "如要幫Prelude X系列行動電源本身充電，建議使用20W以上充電頭;可用Type-C to Type-C線或是USB-A to Type-C線;可以使用PD快充(建議使用 20W充電插頭(符合PD快充) 為最佳體驗。提供安培數參考： 5V 3A 、9V 2.2A)"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "其他MagSafe充電器也可以幫Prelude X/XR無線充電，但Qi因較難對準，所以還是會建議用MagSafe無線充電器去充。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude X系列行動電源無法直充Apple Watch，因為充電模組不一樣"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude X產品磁吸力是與Apple 原廠MagSafe 的產品一致的"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude 系列行動電源反面部分無MagSafe輸出，但有MagSafe輸入，也有無線輸出"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "三明治充電的情境下僅可使用XS的type C供電。(X/XR行動電源則無法使用此方式分別供電，因為XS在幫X/XR充電，如再用type C充電會導致充電效率較低)"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "(Prelude X 系列行動電源背面不建議充手機，背面主要設計場景是給耳機使用，)若要同時為兩台iPhone充電，可一台MagSafe無線充電，另一台有線充電"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "電子檔說明書:Prelude X 電子說明書：https://bit.ly/3vd2uAd;Prelude XR 電子說明書：https://bit.ly/3PKX8pb;Prelude XS 電子說明書：https://bit.ly/3joEl75;Omnia X 電子說明書:https://drive.google.com/file/d/1iio5tPnhO16BG99bMERqzp6rYW4EBNQT/view?usp=sharing;85W車充說明書:https://drive.google.com/file/d/1HABPl9xhH30Q-yUqkEeRYc9k1c8yjaTA/view?usp=sharing(舊版說明書燈號顯示是綠色，新版燈號顯示是藍色）"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude X系列行動電源通過的認證:台灣 BSMI、NCC  認證;日本 PSE 認證;美國 FCC、CE 認證;韓國 KC 認證"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude XR 無線充電充到滿大約6小時，有線充對電部分使用XS對XR線充大約 3小時半;Prelude X 無線充電充到滿大約3小時，有線充電部分使用XS對X線充大約 2小時"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "MagSafe圖示表示為快充，一般充電圖示表示為一般充電，電量如果達80%以上蘋果手機會有電池保護機制，故會出現一般充電圖示，手機處於低電量MagSafe才會容易觸發"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "維修日大約5-7個工作天，如工程師業務量較大，維修工作天數需等待較長時間，日期以實際收到商品開始計算"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude X 系列行動電源重置的方法:先長按電源鍵6~8秒後，再插入c to c 線對X充電10秒即可"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "如何在flyingV取消訂單:發信至 flyingfive@ontoo.cc 告知＂退款原因＂，同時附上您贊助的「專案名稱、金流單號、贊助金額」。退款作業需 1~3 個工作天（不包含例假日），完成退款程序將回覆 Email 通知。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "flying V 海外募資運費計算:香港：運費450元，澳門：運費400元，馬來西亞：運費450元，中國：運費300元"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "如何在flyingV修改訂單內容:請回到 贊助紀錄 頁面，點入訂單右側的「修改」，專案結束日期後的兩天內均可修改您的：收件人姓名、電話、地址、備註資訊以及回饋調查項目。▲專案結束兩天以上之訂單右側會顯示為「查看」，代表無法再修改。仍需更改收件資訊請回到專案頁，至【留言】頁面留言或點選【聯絡提案人】，會由提案人親自為您處理。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "flyingV折扣碼使用方式：進入頁面連結後，選擇限時超早鳥方案->註冊 / 登入 flyingV 會員->在結帳頁面的「優惠碼」欄位輸入上方專屬序號。注意：每次贊助只能使用一組折扣優惠碼。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "flyingV打統編的方式：下單時將單位統編備註於「備註欄位」中。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "【匯款資訊】銀行：台北富邦銀行 西湖分行（銀行代號 012）;戶名：倍加能股份有限公司;帳號：668120008456匯款後請提供後5碼，協助後續查帳，謝謝"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Futura S MagSafe 磁吸無線快充充電盤線長度為90cm"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "如果對方詢問合作意願，你要回:您好，麻煩請您將合作方式、貴司簡報或者影片範例Mail給我們，信箱資訊:info.tw@bezalel.co，會有專人接洽，因LINE訊息容易漏信。期待有機會與您合作，謝謝。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude X系列行動電源均採用鋰聚合物電池，相較於18650電芯，鋰聚合物電池會更安全。另外產品搭載多重安全保護機制，有過充、過熱現象會自動斷電保護電池，同時擁有多國國家安全認證。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "如果有人請你介紹BEZALEL倍加能，你要回:BEZALEL倍加能是美國無線充電科技品牌，專注於高品質、創新兼具美感和功能的無線充電產品。簡約設計風格和匠心打造為特色，實現「無線新生活，新世界」的願景。"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "若對方要查詢他的產品是否還有保固，你要回:您好，請提供訂單以下資訊:訂單編號、訂購平台、訂購姓名、訂購電話。請稍候客服專員會盡快回覆您客服服務時間：週一～週五 8:30am～17:30pm"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "若對方要查詢保固，有提供訂單編號、訂購電話、訂購姓名其中一個資料，你要回:請稍候客服專員會盡快回覆您客服服務時間：週一～週五 8:30am～17:30pm"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "不可以先購買一顆新的行動電源，待原商品維修完再做退貨"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude S系列行動電源可以寄送香港、澳門、馬來西亞"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude S 行動電源（5000 mAh)：額定容量:5V/3000mAh,9V/1600mAh，USB-C輸入:5V/3A,9V/2A，無線輸出:5W/7.5W/10W/15W，USB-C輸出:5V/2.4A,9V/2.22A;Prelude SR行動電源（10000 mAh)：額定容量:5V/6200mAh,9V/3300mAh，USB-C輸入:5V/3A,9V/2A，無線輸出:5W/7.5W/10W/15W，USB-C輸出:5V/2.4A,9V/2.22A"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "Prelude S系列行動電源提供電量顯示，分別有四顆指示燈表示電量，當只有第一顆快速閃爍時，代表電量低於10%，當只有第一顆恆量時，代表電量介於10~25%，當只有第一、二顆恆量時，代表電量介於25~50%，當只有第四顆不量時，代表電量介於50~75%，四顆指示燈全亮，代表電量介於75~100%"},
                    {"role": "assistant", "content": "記住了!"},
                    {"role": "user", "content": "接下來回覆盡量簡潔明瞭，遇到句號要換行，該換行的時候要換行，傳連結前也要換行。"},
                    {"role": "assistant", "content": "記住了!"},
                ]


            else:
                messages = chatgpt

            if msg == '!清空':
                reply_msg = TextSendMessage(text='對話歷史紀錄已經清空！')
                fdb.delete(user_chat_path, None)

            else:
                messages.append({"role": "user", "content": msg})
                response = openai.ChatCompletion.create(
                    model="gpt-4o-2024-08-06",
                    max_tokens=1024,
                    temperature=0.5,
                    messages=messages
                )
                ai_msg = response.choices[0].message.content.replace('\n', '')
                messages.append({"role": "assistant", "content": ai_msg})
                reply_msg = TextSendMessage(text=ai_msg)
                # 更新firebase中的對話紀錄
                fdb.put_async(user_chat_path, None , messages)

            fdb.put_async(chat_state_path, 'last_interaction', current_time.strftime('%Y-%m-%d %H:%M:%S.%f'))
            line_bot_api.reply_message(tk, reply_msg)

        # 處理圖片訊息
        elif msg_type == 'image':
            reply_msg = TextSendMessage(text='好的，謝謝您傳的圖片，之後我們會將您的狀況傳遞給相關人員處裡。')
            line_bot_api.reply_message(tk, reply_msg)

        else:
            reply_msg = TextSendMessage(text='謝謝!')
            line_bot_api.reply_message(tk, reply_msg)

    except Exception as e:
        detail = e.args[0]
        print(detail)
    return 'OK'
