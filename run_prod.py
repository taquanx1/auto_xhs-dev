from app import create_app, api
from flask import Flask, request, render_template
import json

app = create_app()

def generate_notes(seed_dic, model) -> str:
    """
    把用户输入拼成一段示例笔记内容。
    这里你可以替换为真正调用 AI 服务的逻辑。
    """

    # 调用 AI 服务生成笔记内容
    content = api.xhs_note_gen(seed_dic, model=model)
    return content


@app.route("/generate", methods=["POST"])
def generate():
    location = request.form.get("location", "").strip()
    subject = request.form.get("subject", "").strip()
    count = int(request.form.get("count", "1"))
    attributes = request.form.get("attributes", "").strip()
    options = request.form.getlist("options")
    model = request.form.get("model", "sonar-pro")

    print("location:", type(location), location)
    print("subject:", type(subject), subject)
    print("count:", type(count), count)
    print("attributes:", type(attributes), attributes)
    print("options:", type(options), options)


    # Formating
    attributes = attributes.replace("，", ",").replace(",", "\n").replace(" ", "")
    attributes = attributes.split("\n")

    # Pack the seed_dic
    seed_dic = {
        "location": location,
        "subject": subject,
        "count": count,
        "attributes": attributes,
        "options": options
    }

    # 生成笔记内容
    content = generate_notes(seed_dic, model)
    #content = content.replace("**", "")
    #content = content.split('###')[1:]
    #head_list = [ c.split('\n')[0].replace('  ', '+').replace(' ', '+') for c in content ]
    #content = '-------------\n'.join(content)

    out_content = ''
    head_list = []
    content_json = json.loads(content)
    out_content += f"## {content_json['main_title']}\n\n"
    for i in range(1, int(count) + 1):
        cur_title_key = f'item_title_{i}'
        cur_content_key = f'item_content_{i}'
        if cur_title_key in content_json and cur_content_key in content_json:
            head_list.append(content_json[cur_title_key])

            cur_title = content_json[cur_title_key]
            cur_item_content = content_json[cur_content_key]
            out_content += f"{str(i+1)}. {cur_title}\n"
            out_content += f"{cur_item_content}\n\n"
    content = out_content.replace('**', '').replace('##', '')

    _content = '''
## 清迈躺平慢生活·轻奢风格美食探店（5家必吃小吃店推荐攻略）

清迈是许多慢生活、躺平和轻奢风格旅行者的心头爱。这里不仅节奏舒适，还是各类泰北美食的天堂！本篇我将用📒 bullet p【地址】等超实用信息，每家都是精选，助你玩转“慢生活x美食”两不误！

---

### 1. 凤飞飞猪脚饭

- **推荐指数**：⭐️⭐️⭐️⭐️⭐️（超高人气，必吃NO.1！）
- **特点介绍**：
  - 路边摊风情，气氛随意自在，是清迈最经典的夜宵地标。
  - 猪脚炖得软烂，肥而不腻，配上溏心蛋和酸菜，层次超级丰富，连米饭都裹满酱汁。
  - 老板娘标志性的牛仔帽，辨识度高（拍照也很有Feel）！
- **小吃来历**：
  - 这家猪脚饭因为老板娘酷似台湾歌手凤飞飞而得名，几十年如一日手艺，被誉为清迈夜市的灵魂美味。
- **营业时间**：
  - 晚市限定，一般为18:00-凌晨左右，建议早点去，人气超旺常排队。
- **地址**：
  - 古城北门Chang Phuak Gate夜市内，摊位很好找。
- **我的建议**：
  - 人多时别退缩，耐心等候绝对值得！
  - 酱汁可多要一点，更下饭～
  - 不辣可提前说明，清迈有些酸辣酱偏辣。
- **加分Tips**：
  - 拍照建议选夜色刚亮灯时，氛围感最足，记得给老板娘也来一张！

---

### 2. Trok Chang Moi Noodles（猪蹄面名店）

- **推荐指数**：⭐️⭐️⭐️⭐️⭐️
- **特点介绍**：
  - 以招牌猪蹄面著称，猪蹄慢炖到软烂，胶原蛋白满分🌟，入口即化。
  - 店内环境宽敞舒适，性价比高，份量充足。
  - 绿咖喱牛肉米线、猪肉丸面也颇受欢迎，辣而不燥，适合喜欢泰北风味的朋友。
- **小吃来历**：
  - 传承自清迈传统家族食谱，将北部卤味与泰式面条完美结合，开业多年口碑一直很好。
- **营业时间**：
  - 9:00 – 16:30（周三休息），午餐、下午茶时段最佳。
- **地址**：
  - Chang Moi区（建议提前用Google Map导航）。
- **我的建议**：
  - 必点猪蹄面与绿咖喱牛肉米线！
  - 氛围自在，适合一人小坐慢慢享用。
- **加分Tips**：
  - 午餐高峰早去能避开排队。拍照选猪蹄特写，卖相超级诱人！

---

### 3. Khao Soi Lung Prakit Kad Kom（米其林推荐牛肉咖喱面）

- **推荐指数**：⭐️⭐️⭐️⭐️⭐️（米其林推荐！）
- **特点介绍**：
  - 超过40年老店，清迈牛肉Khao Soi咖喱面传奇级别。
  - 牛肉软嫩，咖喱汤底浓郁带微辣，搭配炸脆面条和酸菜、柠檬，风味层次非常丰富。
- **小吃来历**：
  - Khao Soi是清迈最具代表性的北泰米粉，融合缅甸、中华与泰式风味，属于泰北独有面食。
- **营业时间**：
  - 一般为10:00-16:00，建议午餐时段前往，新鲜出锅味道更正！
- **地址**：
  - Kad Kom Market周边（具体可谷歌“Khao Soi Lung Prakit Kad Kom”）。
- **我的建议**：
  - 一定配酸菜和柠檬一起吃，更提味。
  - 店铺不豪华，看重的是味道，躺平慢吃最好不过。
- **加分Tips**：
  - 拍照时记得将面条、汤底和配菜一起拍，色彩层次感特别强。

---

### 4. Busarin at Magnolia Café（精致泰北家族菜）

- **推荐指数**：⭐️⭐️⭐️⭐️（米其林推荐，环境优雅）
- **特点介绍**：
  - 主打正宗泰北菜，由家族食谱传承，环境非常文艺清新，静谧舒适，极适合慢享生活。
  - 招牌“Hang Lay Pork Curry”搭配Roti和青柠沙拉，非常地道。
  - 用料讲究，手工现做，菜品摆盘精致，适合轻奢路线。
- **小吃来历**：
  - Hang Lay Pork Curry起源自缅甸与兰纳王朝美食融合，泰北传统宴席必备，是清迈家常菜的代表。
- **营业时间**：
  - 11:00-22:00（建议提前预约，尤其晚餐时段）
- **地址**：
  - Magnolia Café内（具体定位“Busarin Chiang Mai”）。
- **我的建议**：
  - 适合情侣或轻奢风格小团体聚餐。
  - 推荐多点几道菜一起Share，体验更多风味。
- **加分Tips**：
  - 店内光影极佳，非常适合拍照发小红书，文青氛围满分！

---

### 5. Fruiturday（芒果控天堂·夏日甜品店）

- **推荐指数**：⭐️⭐️⭐️⭐️
- **特点介绍**：
  - 各类芒果甜品一应俱全，从芒果沙冰、奶昔、冰淇淋到芒果糯米饭，颜值超高，甜而不腻，消暑利器🥭。
  - 装修风格可爱明快，非常适合打卡拍照，小情侣、闺蜜组团首选！
- **小吃来历**：
  - 清迈盛产芒果，芒果糯米饭、芒果甜品已成为地标级美食，几乎每家店都有自家拿手做法。
- **营业时间**：
  - 10:00-22:00
- **地址**：
  - Rachadamnoen Rd, Tha Phae Gate附近（老城区核心地段）
- **我的建议**：
  - 强烈推荐芒果糯米饭和芒果奶昔，性价比高，份量实在。
  - 夏天中午吃最舒服，补充水分解暑佳品。
- **加分Tips**：
  - 店内彩色墙面适合拍照，甜品颜值高，晒朋友圈获赞无数！

---

## 总结 · 我的清迈慢生活美食体验建议

- 清迈小吃店大多价格亲民，环境轻松，适合躺平式慢旅行。无论是露天路边摊还是文艺精致餐厅，都有各自独特的美味与氛围。
- 慢节奏旅行建议每天只安排2-3家小吃店，一边散步一边觅食，感受清迈最舒服的慢生活氛围。
- 别忘了多拍照、拍视频，清迈美食颜值很高，分享记录超有成就感🎬📸！
- 推荐带一本本地小吃手账本，每尝试一家，就写下你的评分和小感受，体验感升级。
- 芒果甜品类、咖喱面、猪脚饭、家常北泰菜都是不可错过的经典，如果时间有限，建议优先按推荐指数选择。
- 清迈多数小吃店休息日不同，记得提前查好营业时间，避开中午和晚餐高峰。

---

### 你最想打卡哪家？或者你有其他宝藏清迈美食推荐，欢迎留言一起交流！下次再来清迈，记得带着这篇攻略慢慢逛、慢慢尝、慢慢享受吧～🦋🍴🌴
    '''

    # 渲染到可编辑页面
    return render_template("result.html", content=content, head_list=head_list)

if __name__ == '__main__':
    app.run(debug=True)
