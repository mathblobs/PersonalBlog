from flask import Flask, render_template, url_for, request, redirect, jsonify, Response
import json
import os

app = Flask(__name__)

USERNAME = "admn"
PASSWORD = "password"

# Implementing basic http authentication

def checking_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response('Could not verify your access level. Please provide valid credentials.', 401, 
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})

# First Information
def define_first_article():
    data = {"1": {"title": "The Power of Hard Work in Building a Great Company", "date": "25.04.2024", "content": '''Creating a truly great company is a challenging journey that demands more than just talent, vision, or resources—it requires an extraordinary amount of hard work. 
            While many people dream of entrepreneurial success, very few actually achieve it, and the key differentiator often comes down to the willingness to work harder, 
            longer, and smarter than anyone else. Hard work is the engine that drives the transformation from an idea into a thriving business, 
            shaping the foundation for sustainable growth, innovation, and resilience. Building Strong Foundations
            When starting a company, hard work is essential in laying down a solid foundation. At the early stages, the founder often has to wear multiple hats, 
            managing everything from product development to customer service, finance, and marketing. There’s no room for complacency in the initial phases; 
            building a company requires founders to learn continuously, adapt quickly, and put in long hours to keep things moving forward. 
            Hard work is the cornerstone of mastering these diverse responsibilities, which ensures that the company’s growth rests on a stable and well-established base.
            Furthermore, hard work is essential to creating a company culture that values commitment and diligence. When employees see the founder’s dedication and drive, 
            hey’re more likely to adopt these qualities themselves. This commitment to hard work becomes a part of the company’s DNA, 
            shaping a culture that pushes each person to go above and beyond. The energy, work ethic, and commitment from the early days become the company’s bedrock, 
            inspiring employees to contribute their best and be fully invested in the company’s success.
            Developing Resilience
            The journey of building a company is filled with obstacles, setbacks, and failures. Hard work doesn’t just involve doing the job; 
            it also means persevering in the face of challenges and bouncing back from failures. Without a strong work ethic, 
            the natural setbacks that every business encounters could easily derail progress. 
            Hard work is what pushes a founder to continue innovating, pivoting, and adapting to market demands, even when things aren’t going as planned.
            Every great company has a story of resilience—times when the founder could have given up but chose to keep working through the difficulty. 
            Hard work fuels this resilience, giving founders the grit to face the ups and downs of entrepreneurship. Building a great company is a long game, 
            and only those who are committed to working hard over the long term can push through the low points to come out stronger and more capable.
            Gaining a Competitive Edge
            In the world of business, competition is fierce. Regardless of the industry, countless other companies are vying for the same customers, market share, and investor interest. 
            Hard work provides a competitive edge, allowing founders to create a unique value proposition, refine their product, and build relationships with customers. 
            The more time, energy, and effort a founder invests in their company, the better they understand their market, customers, and competition. 
            This deep understanding often translates into innovative solutions and a superior product that stands out among competitors.
            Moreover, hard work shows commitment, which can attract the right partners, investors, and employees. People want to be part of something special, 
            and when they see a founder’s unwavering dedication, they’re more likely to trust in the company’s potential. Investors, especially, 
            look for founders who have the drive to see their vision through to completion. Hard work, then, becomes a signal of reliability and potential, 
            attracting resources and relationships that can accelerate the company’s growth.
            Sustaining Long-Term Success
            Building a great company is not just about getting started; it’s about sustaining success over the long term. Hard work is a continual commitment, 
            and the companies that truly excel are those whose founders continue working hard even after achieving initial success. This ongoing effort is what drives continuous improvement, 
            allowing companies to stay relevant in a rapidly changing world. Many companies fail because their founders rest on their laurels after initial success, 
            assuming the business will continue growing on its own. However, companies that succeed over decades are typically those where hard work remains a core value, 
            fostering a culture of innovation, excellence, and adaptability.
            Additionally, customer expectations and market demands are always evolving, and maintaining high standards requires constant effort. Hard work is needed to keep innovating, 
            refining the product, and finding new ways to create value for customers. This commitment to excellence and improvement is what separates a great company from a good one. 
            By continually putting in the effort to meet and exceed customer expectations, a company builds a loyal customer base that becomes a vital asset over time.
            Conclusion
            Hard work is the bedrock of building a great company. It is the catalyst for establishing a strong foundation, developing resilience, gaining a competitive edge, and sustaining 
            long-term success. While many factors contribute to a company’s growth, hard work is the most essential. It takes unwavering dedication, a willingness to endure challenges, 
            and an unrelenting drive to improve and adapt. Founders who embody these qualities not only build successful companies but also create legacies that inspire and empower others. 
            In the end, hard work is not just about achieving milestones; it is the engine that transforms vision into reality, and dreams into lasting impact.'''}}
    save(data)

def ID_Algorithm(firstDict, addedDict):
    ids = []
    for i in firstDict.keys():
        ids.append(int(i))
    if not ids:
        return {"1", addedDict}
    else:
        new_id = max(ids) + 1
        firstDict[str(new_id)] = addedDict
        return firstDict

def load():
    if os.path.exists('ArticleDataBase.json'):
        with open('ArticleDataBase.json', "r") as file:
            return json.load(file)
    return []

def save(information):
    with open('ArticleDataBase.json', "w") as file:
        json.dump(information, file)

@app.route('/home', methods=['GET', 'POST'])
def home():
    data = load()
    if request.method =='POST':
        print("Hello There")
    return render_template('home.html', data = data)

@app.route('/ChosenArticle', methods=['GET', 'POST'])
def article_side():
    data = load()
    id = request.args['item_id']
    return render_template('Article.html', data=data, id=id)

@app.route('/admin', methods=['GET', 'POST'])
def admin_side():
    auth = request.authorization

    if not auth or not checking_auth(auth.username, auth.password):
        return authenticate()
    data = load()
    return render_template('admin.html', data=data)


@app.route('/new_side', methods=['GET', 'POST'])
def new_side():
    data = load()
    if request.method == 'POST':
        new_entry = {"title": request.form.get('TitleNew'),
                    "date": request.form.get('DateNew'),
                    "content": request.form.get('ContentNew')}
        data = ID_Algorithm(data, new_entry)
    save(data)
    print("form data:", request.form)
    return render_template('new.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit_side():
    data = load()
    id = request.args.get('param')
    if request.method == 'POST':
        updated_entry = {"title": request.form.get('UpdatedTitle'),
                        "date": request.form.get('UpdatedDate'),
                        "content": request.form.get('UpdatedContent')}
        data[id] = updated_entry
    save(data)
    return render_template('Editing.html')

@app.route('/delete_page', methods=['GET', 'POST'])
def delete_article():
    data = load()
    id = request.args.get('param')
    del(data[id])
    save(data)
    return redirect(url_for('admin_side'))

if __name__ == "__main__":
    app.run(debug=True)