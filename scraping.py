from DrissionPage import ChromiumPage
from dotenv import load_dotenv
import time
import os

load_dotenv()

def tradingview_auto_login(email, password):
    # 1. ตั้งค่าพื้นฐานและเปิดหน้าเว็บ
    page = ChromiumPage()
    page.get('https://www.tradingview.com/')
    
    try:
        # Step 2: กดปุ่มเมนูผู้ใช้ (ปุ่ม Anonymous)
        # ใช้จุด (.) เชื่อมคลาสที่เว้นวรรคเข้าด้วยกัน
        user_menu = page.ele('.tv-header__user-menu-button tv-header__user-menu-button--anonymous js-header-user-menu-button')
        user_menu.click()
        print("✅ Step 2: กดเมนู Anonymous เรียบร้อย")
        time.sleep(1)

        # Step 3: กดเลือกเมนู Sign in (labelRow)
        login_opt = page.ele('.label-mDJVFqQ3 label-jFqVJoPk label-mDJVFqQ3 label-YQGjel_5 js-main-menu-dropdown-link-title')
        login_opt.click()
        print("✅ Step 3: เลือกเมนู Sign in เรียบร้อย")
        time.sleep(2)

        # Step 4: กดปุ่ม Email Login
        username_field = page.ele('@name=id_username', timeout=2)

        if not username_field:
            print("🔍 ยังไม่เห็นช่องกรอกข้อมูล กำลังมองหาปุ่ม Email...")
            # ถ้าไม่เห็นช่องกรอก ให้มองหาปุ่ม Email Login แล้วกด
            # ใช้ Selector แบบหาจากข้อความจะ "นิ่ง" กว่า class ยาวๆ ครับ
            email_btn = page.ele('text:Email') or page.ele('text:อีเมล') or page.ele('.emailButton-nKAw8Hvt')
            
            if email_btn:
                email_btn.click()
                print("✅ Step 4: กดปุ่ม Email Login เรียบร้อย")
                time.sleep(1)
            else:
                print("⚠️ หาปุ่ม Email ไม่เจอ แต่อาจจะข้ามไปหน้ากรอกข้อมูลเลยก็ได้")

        # Step 5: กรอก Email และ Password
        # ปกติช่องกรอกจะมี name='id_username' และ 'id_password'
        page.ele('@name=id_username').input(email)
        page.ele('@name=id_password').input(password)
        print("✅ Step 5: กรอกข้อมูลสำเร็จ")

        # กดปุ่มยืนยันการ Login (มักจะเป็นปุ่ม submit)
        page.ele('.submitButton-LQwxK8Bm button-D4RPB3ZC large-D4RPB3ZC black-D4RPB3ZC primary-D4RPB3ZC stretch-D4RPB3ZC apply-overflow-tooltip apply-overflow-tooltip--check-children-recursively apply-overflow-tooltip--allow-text apply-common-tooltip').click()

        if page.wait.ele_deleted('.tv-header__user-menu-button--anonymous'):
            print("🎉 ยินดีด้วยนาย! Login สำเร็จแล้ว")
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดหรือ login ไว้อยู่แล้ว: {e}")
    
    return page

def USA(page):
# รายชื่อกลุ่มที่นายต้องการ
    sectors = {
        "Technology_USA": "SP-S5INFT",
        "Financials_USA": "SP-SPF",
        "HealthCare_USA": "SP-S5HLTH",
        "Energy_USA": "SP-SPN",
        "Consumer Staples_USA": "SP-S5CONS",
        "Consumer Discretionary_USA": "SP-S5COND",
        "Industrials_USA": "SP-S5INDU",
        "Materials_USA": "SP-S5MATR",
        "Communication_USA": "SP-S5TELS",
        "Utilities_USA": "SP-S5UTIL",
        "Real Estate_USA": "SP-S5REAS",
    }

    results = {}

    try:
        for name, symbol in sectors.items():
            print(f"กำลังดึง: {name}")
            # เปลี่ยน URL ให้ตรงตาม Format ของ TradingView
            url = f"https://th.tradingview.com/symbols/{symbol}/components/"
            page.get(url)
            time.sleep(2) 
            
            # ดึง Ticker จาก href เหมือนเดิมเพื่อให้ได้ Exchange (NASDAQ/NYSE)
            tickers = page.eles('tag:a@@class=apply-common-tooltip tickerNameBox-GrtoTeat tickerName-GrtoTeat')
            
            sector_stocks = []
            for t in tickers:
                href = t.attr('href')
                if href and '/symbols/' in href:
                    # แปลงจาก /symbols/NASDAQ-AAPL/ เป็น NASDAQ:AAPL
                    raw = href.split('/')[-2]
                    sector_stocks.append(raw.replace('-', ':'))
            
            results[name] = sector_stocks
            print(f"✅ ได้มา {len(sector_stocks)} ตัว")

        return results

    except Exception as e:
        print(f"❌ พลาดตรงกลุ่ม {name}: {e}")
        return results
        
def THAI(page):
    # 1. นิยามกลุ่มอุตสาหกรรมไทยตามที่นายให้มา
    # Key คือชื่อที่จะใช้ใน Dictionary, Value คือส่วนท้ายของ URL ในเว็บ SET
    thai_sectors = {
        "Technology_Thai": "TECH",
        "Financials_Thai": "FINCIAL",
        "HealthCare_Thai": "HELTH",
        "Energy_Thai": "ENERG",
        "Consumer Staples_Thai": "AGRO",
        "Consumer Discretionary_Thai": "CONSUMP",
        "Industrials_Thai": "INDUS",
        "Property_Thai": "PROPCON",
        "Services_Thai": "SERVICE",
    }

    results = {}

    try:
        for name, sector_code in thai_sectors.items():
            print(f"🔍 กำลังดึงกลุ่มไทย: {name} ({sector_code})...")
            
            # URL สำหรับดูรายชื่อหุ้นในแต่ละดัชนีกลุ่มอุตสาหกรรม
            url = f"https://www.set.or.th/th/market/index/set/{sector_code}"
            page.get(url)
            
            # รอโหลดข้อมูลตาราง (เว็บ SET โหลดค่อนข้างไว)
            time.sleep(2) 
            
            # ดึงรายชื่อหุ้นจากตาราง 
            # ในเว็บ SET หุ้นแต่ละตัวจะอยู่ในแท็ก <a> ที่มีลิงก์ไปหน้า Quote
            # เราจะหาแท็ก <a> ที่มีคำว่า /product/stock/quote/ อยู่ใน href
            elements = page.eles('.symbol pt-1')
            
            sector_stocks = []
            for el in elements:
                symbol = el.text.strip()
                # กรองเอาเฉพาะตัวย่อหุ้น (ป้องกันข้อมูลขยะหรือชื่อซ้ำ)
                if symbol and symbol not in sector_stocks and len(symbol) < 15:
                    # เติม Prefix 'SET:' เพื่อให้พร้อมใช้กับ tvDatafeed ในระบบของนาย
                    sector_stocks.append(f"SET:{symbol}")
            
            results[name] = sector_stocks
            print(f"✅ ได้มา {len(sector_stocks)} ตัว")
            print("-" * 20)

        return results

    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในกลุ่ม {name}: {e}")
        return results

def close_investing_popup(page):
    # รายชื่อคลาสหรือ Selector ของปุ่มปิดที่มักจะเจอใน Investing
    close_selectors = [
        '@data-test=sign-up-dialog-close-button',
        'tag:svg@@data-test=sign-up-dialog-close-button',
        'css:svg[data-test="sign-up-dialog-close-button"]'
        '.float-end mr-[-11px] mt-[-24px] w-4 cursor-pointer text-gray-400 hover:text-v2-gray-dark sm:mr-[-20px] relative top-[-45px] self-end',
    ]
    
    for selector in close_selectors:
            close_btn = page.ele(selector, timeout=1)
            if close_btn:
                try:
                    # บางครั้ง svg กดตรงๆ ไม่ติด อาจต้องกดที่ตัวแม่ (Parent) ของมัน
                    close_btn.click()
                    print("🛡️ ปิด Popup ด้วย data-test เรียบร้อย")
                    time.sleep(1)
                    return # ปิดได้แล้วให้ออกเลย
                except:
                    # ถ้าคลิกตัวมันเองไม่ติด ลองคลิกด้วย JavaScript (วิธีนี้จะทะลุผ่านทุกอย่าง)
                    page.run_js('arguments[0].click();', close_btn)
                    print("🛡️ ปิด Popup ด้วย JS Click เรียบร้อย")
                    return
            
def CHINA(page):
    # 1. นิยาม URL Slugs ของ Investing.com สำหรับแต่ละกลุ่ม
    # หมายเหตุ: URL ของ Investing มักจะใช้ชื่อเต็มของกลุ่ม
    china_sectors = {
        "Technology_China": "hsci-info-tech",
        "Financials_China": "hsci-financials",
        "HealthCare_China": "hang-seng-industry-healthcare-tr",
        "Energy_China": "hsci-energy",
        "Consumer Staples_China": "hsci-industry-consumer-staples",
        "Consumer Discretionary_China": "hsci-consumer-discretionary",
        "Telecommunications_China": "hsci-tele",
        "Industrials_China": "hsci-indu-good",
        "Materials_China": "hsci-materials",
        "Utilities_China": "hsci-utilities",
        "Properties_Construction_China": "hsci-prop---con",
        "Conglomerates": "hsci-cong"
    }
    
    page.set.window.max()
    
    results = {}
    count = 0
    try:
        while count == 0:
            for name, slug in china_sectors.items():
                print(f"🔍 กำลังดึงกลุ่มจีน: {name}...")
                
                # URL สำหรับหน้า Components ของดัชนีนั้นๆ
                url = f"https://www.investing.com/indices/{slug}-components"
                page.get(url)
                time.sleep(2)
                
                # --- แก้ปัญหา Popup ที่นี่ ---
                close_investing_popup(page)
                # ---------------------------
                
                # 1. คลิกเปิด Dropdown (จุดที่นายทำไว้แล้ว)
                filter_btn = page.ele('.p-0 h-3 w-3')
                filter_btn.click()
                time.sleep(1) # รอให้เมนู Dropdown เด้งขึ้นมา

                # 2. หา "ทุกตัวเลือก" ที่อยู่ใน Dropdown นั้น
                # แนะนำให้ใช้คลาสหลักที่สั้นลง หรือใช้โครงสร้างที่ระบุถึงตัวเลือกในลิสต์
                options = page.eles('.w-full cursor-default dropdown_noSelect__rU_0Y bg-white hover:bg-[#deebff] px-5 py-2 hover:cursor-pointer')

                # 3. คลิกเลือก "อันสุดท้าย" ในลิสต์
                if options:
                    print(f"พบตัวเลือกทั้งหมด {len(options)} อัน กำลังเลือกอันสุดท้าย...")
                    options[-1].click() # [-1] คือการเลือกสมาชิกตัวสุดท้ายใน List
                    time.sleep(1) # รอให้ตารางรีโหลดข้อมูลใหม่
                else:
                    print("❌ หาตัวเลือกใน Dropdown ไม่เจอ")
                
                # ดึงรายชื่อหุ้นจากตาราง
                # ปกติรหัสหุ้นฮ่องกงใน Investing จะอยู่ในคอลัมน์ "Symbol" 
                # ซึ่งมักจะอยู่ในแท็ก <td> ที่มีคอลัมน์ชื่อ 'bold left noWrap elp' 
                # หรือเราจะดึงจากทุกลิงก์ที่มีคำว่า /equities/
                elements = page.eles('.block overflow-hidden text-ellipsis whitespace-nowrap')
                
                sector_stocks = []
                for el in elements:
                    symbol = el.text.strip()

                        # เติม Prefix 'HKG:' เพื่อให้ใช้กับ tvDatafeed (ส่วนใหญ่หุ้นกลุ่มนี้เทรดที่ HK)
                        # แต่ต้องระวังบางตัวอาจจะเป็นตลาดอื่น นายอาจจะต้องปรับตามความเหมาะสม
                    sector_stocks.append(f"HKEX:{symbol}")
                
                # กรองข้อมูลซ้ำและเก็บลง Dict
                results[name] = list(set(sector_stocks))
                
                if len(results[name]) > 0:
                    count += 1
                    
                print(f"✅ ได้มา {len(results[name])} ตัว")
                print("-" * 20)
                

        return results

    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดในกลุ่ม {name}: {e}")
        return results