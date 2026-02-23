# test_model.py
from ctransformers import AutoModelForCausalLM

# 1️⃣ Modelin path'i
model_path = "/Users/zeyneppinarsoy/ollama_models/mistral-7b-v0.1.Q4_0.gguf"

# 2️⃣ Modeli yükle
print("Model yükleniyor…")
model = AutoModelForCausalLM.from_pretrained(model_path)
print("Model yüklendi ✅")

# 3️⃣ Test prompt'u
prompt = "Write a short email response for a refund request."
# 4️⃣ Yanıt üret
print("\nPrompt gönderiliyor…")
tokens = model.tokenize(prompt)[:20]

# Token token çıktı üret ve biriktir
output_list = []
for token in model.generate(tokens):
    print(token, end="")  # terminalde anlık gösterim
    output_list.append(token)

# Generator’dan string oluştur
output_text = "".join(output_list)

# 5️⃣ Çıktıyı göster
print("\n\n--- Model Yanıtı ---")
print(output_text)
print("-------------------")

