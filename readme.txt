LOKAL VERSIYON
kodu lokalde çalıştırmak için:
projenin olduğu klasörde öncelikle venv'i aktifleştiriyoruz. 
venv'i aktifleştirmek için komut: 
source venv/bin/activate

ilk defa çalıştıracaksanız eğer önce requirements dosyasını indirmelisiniz. 
Bunun için gerekli komut: 
pip install -r requirements.txt

son versiyonun adı gmail_app.py bunu çalıştırmak için ise:
python gmail_app.py 

çalıştırınca oluşan lokal link'e tıkladığımızda zaten karşımızda projemiz yer alıyor. 
Bu versiyonda mailler otomatik gönderilmiyor, bir approval-send mekanizmasına sahip. 



kendi gmail hesabınızda kullanmanız için gereken:
gmail hesabınızda 2 adımlı doğrulamanın açık olması gerekiyor. 
sonrasında ayarlarda güvenlik ve uygulama şifreleri kısmından 16 haneli bir kod alacaksınız. kesinlikle bir yerde paylaşmayın
bu kodu benim oluşturduğum arayüzde mail şifreniz olarak kulllanacaksınız 

neler yaptım sırasıyla,

1- terminalde ollama indirdik, 
2- ollama pull mistral
3- terminalde test ettik ssi var 
4- sonra vscode içerisinde venv kurup test.py ile test ettik
5-ilk versiyonda 4 adet agent vardı ve mistral 7b versiyonu kullanıyorduk ancak bu şekilde
8 gb ram'e sahip bilgisayarımı biraz zorladı. optimize etmek adına, 
quantized versiyona geçtim sonra vazgeçtim
6- 7b'de kalmaya karar veriyorum nedenleri mediumda yer alıyor 
7- testleri yapıyorum, dil seçeneği eklemeyi deniyorum. son versiyonunda sadece ingilizce destekliyor. agents.py dosyasındaki promptlar değiştirilip dil seçeneği eklenbilir.
8- regex ekledim. username, order no alabiliyor.

