import json
from pathlib import Path

DATA_FILE = Path("papers.json")

def load_papers():
    """
    读取论文数据
    :return:
    """
    if not DATA_FILE.exists():
        return []
    try:
       with open(DATA_FILE, "r",encoding="utf-8") as f:
           papers = json.load(f)

       if not isinstance(papers,list):
           print("数据格式错误:papers.json中应该是一个列表。")
           return []

       return papers

    except json.JSONDecoderError:
        print("papers.json文件格式错误，已使用空论文列表")
        return []

def save_papers(papers):
    """
    把论文列表保存到papers.json中
    """
    with open(DATA_FILE, 'w', encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False,indent=2)
def add_paper(papers):
    """
    添加一篇论文
    :param papers:
    :return:
    """
    title = input("请输入论文标题：").strip()
    if not title:
        print("论文不能为空")
        return

    authors = input("请输入作者，多个作者用逗号分隔：").strip()
    if not authors:
        print("作者不能为空")
        return

    year = input("请输入发表年份：").strip()
    keywords = input("请输入关键词，多个关键词用逗号分隔：").strip()
    if not keywords:
        print("关键词不能为空")
        return

    venue = input("请输入会议或期刊名称：").strip()
    if not year.isdigit():
        print("年份必须是数字：")
        return
    year = int(year)
    if year < 1900 or year > 2026:
        print("年份范围不合理")
        return

    paper={
        "title":title,
        "authors":authors,
        "year":int(year),
        "keywords":[k.strip() for k in keywords.replace('，',',').split(',') if k.strip()],
        "venue":venue
    }
    papers.append(paper)
    save_papers(papers)
    print("论文添加成功!")

def list_papers(papers):
    """
    查看所有论文
    :param papers:
    :return:
    """
    if not papers:
        print("当前还没有论文.")
        return

    for index,paper in enumerate(papers,start=1):
        print(f"\n[{index}]{paper['title']}")
        print(f"作者：{paper['authors']}")
        print(f"年份：{paper['year']}")
        print(f"关键词：{'，'.join(paper['keywords'])}")
        print(f"会议/期刊：{paper['venue']}")

def search_papers(papers):
    '''
    按关键词搜索论文
    :param papers:
    :return:
    '''
    query = input("请输入搜索关键词：").strip().lower()

    if not query:
        print("输入的关键词不能为空。")
        return

    results = []

    for paper in papers:
        title = paper["title"].lower()
        authors = paper["authors"].lower()
        keywords = " ".join(paper["keywords"]).lower()

        if query in title or query in authors or query in keywords:
            results.append(paper)

    if not results:
        print("没有找到相关论文")
        return

    print(f"找到{len(results)}篇相关论文：")
    list_papers(results)

def show_menu():
    print('\n======论文检索小工具======')
    print('1.添加论文')
    print('2.查看所有论文')
    print('3.搜索论文')
    print('4.退出')

def main():
    papers = load_papers()

    while True:
        show_menu()
        choice = input("请输入操作序号:").strip()

        if choice == "1":
            add_paper(papers)
        elif choice == "2":
            list_papers(papers)
        elif choice == "3":
            search_papers(papers)
        elif choice == "4":
            print("已退出。")
            break
        else:
            print("输入无效，请输入 1/2/3/4。")

if __name__ == "__main__":
    main()

