from bs4 import BeautifulSoup
import requests as req
from tqdm import tqdm
import os



class Title():
    '''create a title, and overloaded the "<" a.k.a lt and "=" a.k.a eq operators
    so i could sort them..'''
    def __init__(self,text:str,points:int):
        self.txt=text
        self.points=points
    def __repr__(self) -> str:
        return f'Title(title={self.txt}, points={self.points})'
    def __lt__(self,other:object)->bool:
        if (other==None and self) or (other and self==None):
            return False
        return self.points<other.points
    
    def __eq__(self, other: object) -> bool:
        if (other==None and self) or (other and self==None):
            return False
        return self.points==other.points

    


def get_all_ancors_text(res)->list:
        '''function pasrses html news page and returns 
        an array of titles from thus page'''

        soup=BeautifulSoup(res.text,'html.parser')
        # ancor_string='tr.athing td.title span.titleline >a'
        ancor_string='tr.athing td.title span.titleline >a'
        all_anchors = soup.select(f"{ancor_string}")
        all_scors=soup.select('.score')
        if(len(all_anchors)!=len(all_scors)):
            raise Exception(f'{abs(len(all_anchors)-len(all_scors))} mismatch amount of scores and titles')
        page_titles=[Title(i.text,int(j.text.split(" ")[0])) for (i,j) in zip  (all_anchors,all_scors) ]
        return page_titles
        

def highest_marked():
    NEWS_ROUTE='https://news.ycombinator.com/news?p='
    title_lst=[]
    page_number=1
    line_number=1
    bar = tqdm(total=100)
    while(True): 
        res=req.get(f'{NEWS_ROUTE}{page_number}')
        try:
            page_ancors=get_all_ancors_text(res)
        except Exception as e:
            print(f" page {page_number} caught {e}")
            page_number+=1
            continue

        if len(page_ancors):#there is no error in empty page.. so im checking length of res
            page_number+=1
            title_lst+=page_ancors
            if page_number%100==0:
                bar.reset()
            bar.update(1)
        else:
            bar.set_description(f'Finished, scanned {page_number} pages')
            bar.update(bar.total-bar.n)
            bar.close()
            break

    title_lst.sort()
    os.system("cls||clear")
    for i,j in enumerate(title_lst[-1:-11:-1]):
        print(f"{i+1}. {j} \n")
    



if __name__=="__main__":
    highest_marked()