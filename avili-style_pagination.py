import requests
from bs4 import BeautifulSoup
import os
import shutil
import json


def get_data(url):
    session = requests.Session()
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }
    data = {
        "FORM_SENT": "1",
        "USER_LOGIN": "makaroveg05@gmail.com",
        "USER_PASSWORD": "phuxkjy",
        "AUTH_FORM": "Y",
        "TYPE": "AUTH",
        "backurl": "/auth/",
        "Login": "Войти",
        "USER_REMEMBER": "Y"
    }
    auth_url = "https://www.avili-style.ru/auth/?login"
    ses1 = session.post(auth_url, data=data, headers=headers)
    cookies = [
        {"domain": key.domain, "name": key.name, "path": key.path, "value": key.value}
        for key in ses1.cookies
    ]
    session2 = requests.Session()
    session3 = requests.Session()
    for cookie in cookies:
        session2.cookies.set(**cookie)
        session3.cookies.set(**cookie)
    product_directory = url.split("/")[-2]
    try:
        os.mkdir("files")
        shutil.rmtree("data")
        os.remove("projects.html")
        os.remove("pages.html")
    except:
        pass
    try:
        shutil.rmtree("data")
    except:
        pass
    os.mkdir("data")
    os.mkdir(f"data/{product_directory}")
    pag = session2.post(url, headers=headers)
    with open("pages.html", "w", encoding="utf-32") as file:
        file.write(pag.text)
    with open("pages.html", "r", encoding="utf-32") as file:
        src1 = file.read()
    pages = []
    soup1 = BeautifulSoup(src1, "lxml")
    page = soup1.find("ul", class_="pagination").find_all("span")
    for i in page:
        pages.append(int(i.text))
    max_pages = pages[-1]
    # for json
    product_data_list = []
    # for txt
    # product_data_list = ''
    for i in range(1, max_pages + 1):
        req = session3.post(f"{url}?PAGEN_1={i}", headers=headers)
        product_directory = url.split("/")[-2]
        try:
            os.mkdir(f"data/{product_directory}")
        except:
            pass
        with open("projects.html", "w", encoding="utf-32") as file:
            file.write(req.text)
        with open("projects.html", "r", encoding="utf-32") as file:
            src = file.read()
        soup = BeautifulSoup(src, "lxml")
        products = soup.find_all("div", class_="product-item")
        product_urls = []
        for product in products:
            product_url = "https://www.avili-style.ru" + product.find("div", class_="product-image").find("a", class_="path").get("href")
            product_urls.append(product_url)
        for product_url in product_urls:
            req = session2.get(url=product_url, headers=headers)
            product_name = product_url.split("/")[-2]
            try:
                with open(f"data/{product_directory}/{product_name}.html", "w", encoding="utf-32") as file:
                    file.write(req.text)
                with open(f"data/{product_directory}/{product_name}.html", "r", encoding="utf-32") as file:
                    src = file.read()
                    soup = BeautifulSoup(src, "lxml")
                    product_data = soup.find("div", class_="wrapper")
                    # print(product_url)
                try:
                    product_images = []
                    product_images.append("https://www.avili-style.ru" + product_data.find("a", class_="download_photo").get("href"))
                    # print(product_image)
                    for img in product_data.find("ul", class_="pv-photo-big-list zoom2").find_all("img"):
                        product_images.append("https://www.avili-style.ru" + img.get("src"))
                    # print(product_images)
                except:
                    product_images = "No product images"
                try:
                    product_name = product_data.find("div", class_="pv-name").text
                    # print(product_name)
                except:
                    product_name = "No product name"
                try:
                    product_having_now = product_data.find("div", class_="label-available").text
                    # print(product_having_now)
                except:
                    product_having_now = "Not available"
                try:
                    product_sizes = product_data.find_all("div", class_="input-append spinner")
                    for size in range(len(product_sizes)):
                        product_sizes[size] = int(product_sizes[size].text)
                    # print(product_sizes)
                except:
                    product_sizes = "Not available"
                try:
                    product_price = int(product_data.find("div", class_="pv-price").text.replace(" ", "").split(" ⃏")[0])
                    # print(product_price)
                except:
                    product_price = 0
                # print("#" * 20)

                # for txt
                # product_data_list += f"Название товара: {product_name}\nURL товара: {product_url}\nURL фото товара: {product_images}\nВ наличии / нет в наличии: {product_having_now}\nДоступные размеры: {product_sizes}\nЦена товара: {product_price}\n\n"
                # for json
                product_data_list.append(
                    {"Название товара": product_name,
                     "URL товара": product_url,
                     "URL фото товара": product_images,
                     "В наличии / нет в наличии": product_having_now,
                     "Доступные размеры": product_sizes,
                     "Цена товара": product_price,
                     }
                )
            except:
                pass
    # for json
    with open(f"files/{product_directory}.json", "a", encoding="utf-8") as file:
        json.dump(product_data_list, file, indent=4, ensure_ascii=False)
    # for txt
    # with open(f"files/{product_directory}.txt", "w", encoding="utf-8") as file:
    #     file.write(product_data_list)
    os.remove("projects.html")
    os.remove("pages.html")
    shutil.rmtree("data")


if __name__ == "__main__":
    urls = ["platya", "sarafany", "leto-2017", "vesna-2017", "winter-2017", "vodolazki", "blouses", "skirts", "jacket", "pants"]
    for url in urls:
        try:
            # for json
            os.remove(f"files/{url}.json")
            # for txt
            # os.remove(f"files/{url}.txt")
        except:
            pass
        get_data(f"https://www.avili-style.ru/catalog/{url}/")
