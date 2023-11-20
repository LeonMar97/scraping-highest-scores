from bs4 import BeautifulSoup
import requests as req
from tqdm import tqdm



class Title():
    def __init__(self,text:str,points:int):
        self.txt=text
        self.points=points
    def __repr__(self) -> str:
        return f'Title(title={self.txt}, points={self.points})'
    def __lt__(self,other:object)->bool:
        return self.points<other.points
    
    def __eq__(self, other: object) -> bool:
        return self.points==other.points

    


def get_all_ancors_text(res):
        soup=BeautifulSoup(res.text,'html.parser')
        # ancor_string='tr.athing td.title span.titleline >a'
        ancor_string='tr.athing td.title span.titleline >a'
        all_anchors = soup.select(f"{ancor_string}")
        all_scors=soup.select('.score')
        # if(len(all_anchors)!=len(all_scors)):
        #     raise Exception("")
        page_titles=[Title(i.text,j.text) for (i,j) in zip  (all_anchors,all_scors) ]
        return page_titles
        

def highest_marked():
    title_lst=[]
    page_number=1
    line_number=1
    bar = tqdm(total=100)
    while(True): 
        res=req.get(f'https://news.ycombinator.com/news?p={page_number}')
        page_ancors=get_all_ancors_text(res)
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

    sorted_titles=title_lst.sort()[:10]

    print(*sorted_titles,sep='\n')



if __name__=="__main__":
    highest_marked()