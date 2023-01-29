# 创建Question页为拼写的卡片
1.打开菜单[管理笔记模板]
![img_1.png](img_1.png)

2.在左侧选择对应的笔记模板后，在右侧点击按钮[卡片]
![img_2.png](img_2.png)

3.在右上角选择[添加卡片模板]或在左侧直接编辑已有的卡片模板
![img_3.png](img_3.png)

4.在[正面内容模板]中填入以下内容
```
<div class="spell">{{spell}}</div>
```

5.在[背面内容模板]中填入以下内容
```
<div class="spell">{{spell}}</div>
<div class="pron-and-accent">{{pron}}{{accent}}</div>
<div class="path-of-speech">{{part_of_speech}}</div>
<div>
    <span class="sound">{{sound}}</span>
    <a class="to-moji" href="{{MojiToAnki_link:link}}">
        <i class="iconfont"></i>
    </a>
    <a class="update-word" onclick="pycmd('MojiToAnki_update')" href="#">
        <i class="iconfont"></i>
    </a>
</div>
{{#note}}
<div class="note">{{note}}</div>
{{/note}}
<br/>
{{^examples}}
<div style="font-size: 16px;">{{trans}}{{^trans}}{{excerpt}}{{/trans}}</div>
{{/examples}}
<div>{{examples}}</div>
<script>
    var replayButton = document.getElementsByClassName('replay-button')[0];
    if(replayButton){
        replayButton.innerHTML='<i class="iconfont"></i>';
    }
</script>
<script>
    function changeDisplay(transId) {
        const trans = document.getElementById('trans-' + transId);
        if (trans.style.display === 'none')
            trans.style.display = 'block'
        else
            trans.style.display = 'none'
    }
</script>

<script>
    rtList = document.getElementsByTagName('rt')
    for (let i = 0; i < rtList.length; i++) {
        rtList[i].innerText = rtList[i].getAttribute('hiragana')
    }
</script>
```

6.点击保存