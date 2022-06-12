
--------

所需要的python依赖包在requirements.txt中
可以使用 pip install -r requirements.txt 一次性安装全部

--------
clean_data_and_make_index  是对爬下来的数据 进行一些清晰工作，并且将数据存入数据库，建立索引
    
    这里使用了 sqlite数据库，为了方便数据和项目一同携带
    
searcher.py 简易的web后端， 实现了 

    1 在网页输入搜索关键字， 在后端接收到关键字
    
    2 对关键字进行分词
    
    3 在索引中查找和关键字有关的文档
    
    4 按照余弦相似度 对文档进行排序
    
    5 把相近的文档展示出来

--------
        
1 数据清洗 并 建立索引：

    database.db  是一个sqlite数据库文件
    
    首先将每个文档存到了数据库当中  
    
    数据库表为 page_info(id,keyword, title, url)
    
        id 自增主键 
        
        keyword: 存了该文档文字用jieba分词打散后的词汇列表（用空格隔开所有词语的字符串）
        
        title: 文档的文字内容 
        
        url: 该文档的网页链接
        
    然后 把每个文档 使用jieba分词工具， 打散成词语，把所有词语放到一个集合中（集合能去重）
    
        把所有词 存入数据库 建立索引  
        
        索引这样理解：
        
            关键词:  你好  包含关键词的文档： <1,2,6,8,9>
            
        表为 page_index(id, word, page_id)
        
            id: 自增 主键
            
            word: 当前关键词
            
            page_id: 包含该关键词的文档id 也就是page_info.id
            
            
    
2 实现检索：

    首先 使用了bottle框架，是一个非常轻巧的web后端框架，实现了一个简单的web后端
    
    前端页面使用了bootstrap 的css样式，，毕竟自己什么垃圾的一p
    
    检索的实现过程：
    
        1 后端拿到检索的关键词，用jieba分词 把拿到的语句打散成词汇 形成关键词keyword_list
        
        2 在建立的索引表page_index中，搜关keyword_list中出现的词汇的page_id
        
        3 在包含所有keyword的文档上 计算和keyword的余弦相似度，然后降序排列
        
        4 返回给前端显示搜索结果
        
        


