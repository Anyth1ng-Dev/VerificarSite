from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        url_do_site = request.form["url"]
        driver = webdriver.Chrome()
        driver.get("https://www.siteconfiavel.com.br/")
        try:
            campo_busca = driver.find_element(By.XPATH, '//input[@placeholder="Cole o Link/URL do site"]')
            campo_busca.send_keys(url_do_site)
            campo_busca.send_keys(Keys.RETURN)
            time.sleep(10)  # Esperar mais tempo para carregar os resultados
            
            elementos_resultado = driver.find_elements(By.XPATH, '/html/body/app-root/slug-container/app-trust-checker/div/div/app-trust-checker-result-screen/div/div[3]/*')
            dados_resultado = "\n".join([elem.text for elem in elementos_resultado])
        except Exception as e:
            dados_resultado = f"Erro ao processar os dados: {e}"
        finally:
            driver.quit()
        resultado = dados_resultado
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
