model_css_class = '''@font-face {
  font-family: HiraMinProN-W6;
  src: url("_HiraMinProN-W6.ttf");
}

@font-face {
  font-family: iconfont;
  src: url("_iconfont.7a6f8a1.ttf");
}

.iconfont {
    font-family: "iconfont" !important;
    font-size: 20px;
    font-style: normal;
    color: #FF5252;
}


.replay-button i:before {
    content: "\e6c6";
}

.to-moji {
    text-decoration: none;
    display: inline-flex;
    vertical-align: middle;
    margin: 3px;
}

.to-moji i:before{
    content: "\e6c7"
}

.card {
    min-height: 100%;
    font-size: 14px;
    font-family: "Hiragino Kaku Gothic Pro",Meiryo,MS Gothic,Tahoma,Arial,PingFangSC-Regular,Microsoft Yahei,"黑体";
    text-align: left;
    color: black;
    background: #f8f8f8;
    display: block;
}

.card.nightMode  {
    color: #fafafc;
    background: #0e0e10;
}


.nightMode .spell, .nightMode .pron-and-accent {
    color: #fafafc;
}

.spell {
    color: #3d454c;
    font-size: 36px;
    font-weight: 600;
    font-family: HiraMinProN-W6,HiraMinProN,'Hiragino Kaku Gothic Pro', Meiryo, MS Gothic, Tahoma, Arial, PingFang SC, '黑体';
}

.pron-and-accent {
    font-size: 16px;
    color: #3d454c;
    line-height: 1.4;
}

.path-of-speech {
    line-height: 3;
}

#sound {
    position:fixed;
    bottom:0;
    left:0;
}

#link {
    position:fixed;
    bottom:0;
    right:30px;
}

.front-trans {
    font-size: 16px;
}

.front-trans li {
    padding-bottom: 10px
}

.word-trans {
    font-size: 16px;
    background: #acacac1a;
    border-radius: 15px;
    padding: 10px;
    margin-bottom: 16px;
}

.nightMode .word-trans {
    background: #acacac1a
}

.example-title {
    padding-left: 16px;
    font-size: 16px;
    line-height: 20px; 
}

.example-trans {
    padding-left: 16px;
    color: #8b8787;
    font-size: 14px;
    line-height: 18px;
    margin-bottom: 24px;
}

.note {
    font-size:15px;
    color: #FF5252;
    border: 1px solid #FF5252;
    border-radius: 15px;
    padding: 10px;
}

.sound {
    float: right
}

ruby rt {
    font-weight: 400;
    font-size: 11px;
    text-align: center;
    font-family: "Hiragino Kaku Gothic Pro",Meiryo,MS Gothic,Tahoma,Arial,PingFangSC-Regular,Microsoft Yahei,"黑体";
}
'''

front_pron = '''<div class="spell">{{pron}}{{accent}}</div>
<div class="sound">{{sound}}</div>
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
'''

front_spell = '''<div class="spell">{{spell}}</div>'''

front_trans = '''<div class="front-trans">{{part_of_speech}}{{trans}}</div>'''

detail = '''<div class="spell">{{spell}}</div>
<div class="pron-and-accent">{{pron}}{{accent}}</div>
<div class="path-of-speech">{{part_of_speech}}</div>
<div>
    <span class="sound">{{sound}}</span>
    <a class="to-moji" href="{{MojiToAnki_link:link}}">
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
'''
