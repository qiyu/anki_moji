model_css_class = '''@font-face {
  font-family: HiraMinProN-W6;
  src: url("_HiraMinProN-W6.ttf");
}

.replay-button svg {
    width: 20px;
    height: 20px;
}

.replay-button svg path {
    fill: #FF5252;
}

.to-moji {
    text-decoration: none;
    display: inline-flex;
    vertical-align: middle;
    margin: 3px;
}

.to-moji svg {
    width: 20px;
    height: 20px;
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
    font-family: HiraMinProN-W6,HiraMinProN;
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
    document.getElementsByClassName('replay-button')[0].innerHTML='<svg t="1670944272402" class="playImage" viewBox="0 0 1137 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="9821" xmlns:xlink="http://www.w3.org/1999/xlink" width="17.765625" height="16"><path d="M798.776889 282.453333a358.513778 358.513778 0 0 1 0 482.816 45.397333 45.397333 0 0 1-19.683556 23.324445 46.193778 46.193778 0 1 1-63.374222-67.015111 269.539556 269.539556 0 0 0 13.312-382.122667 47.502222 47.502222 0 0 1-22.755555-33.621333 47.160889 47.160889 0 0 1 38.912-54.101334 46.421333 46.421333 0 0 1 30.094222 5.404445c10.808889 4.949333 19.285333 14.051556 23.495111 25.315555z m161.564444-168.504889a554.325333 554.325333 0 0 1 153.031111 382.805334c0 167.082667-73.955556 316.529778-190.577777 418.588444l-0.056889-0.113778a46.364444 46.364444 0 0 1-84.878222-26.282666c0-18.261333 10.524444-34.019556 25.827555-41.642667l-0.170667-0.227555a464.384 464.384 0 0 0 159.345778-350.321778 464.042667 464.042667 0 0 0-129.308444-321.649778 47.160889 47.160889 0 1 1 66.844444-61.155556zM464.042667 33.735111C529.408-27.534222 632.035556-2.275556 632.035556 102.684444v818.232889c0 103.936-101.432889 131.527111-168.106667 68.892445l-231.992889-237.340445H90.567111c-59.505778 0-90.225778-33.564444-90.225778-90.282666V361.415111c0-57.742222 29.752889-90.282667 90.225778-90.282667h141.425778L463.985778 33.735111z m77.824 840.931556V151.722667c0-71.111111-30.378667-31.971556-61.098667-1.877334-54.158222 52.963556-135.224889 139.207111-202.126222 211.569778H150.755556c-44.828444 0-60.188444 16.270222-60.188445 60.131556v180.508444c0 44.771556 14.449778 60.131556 60.188445 60.131556h126.407111c67.299556 71.964444 149.105778 158.321778 203.320889 211.797333 31.061333 30.72 61.326222 69.006222 61.326222 0.682667z" p-id="9822"></path></svg>';
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
        <svg t="1670999911770" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="25742" width="16" height="16"><path d="M817.078857 119.954286l-5.266286-4.827429a39.424 39.424 0 0 0-50.395428 2.779429l-24.576 22.893714-4.754286 5.339429-3.657143 5.851428a39.424 39.424 0 0 0 6.363429 44.470857l38.473143 41.252572-36.644572 0.146285-13.312 0.512a245.467429 245.467429 0 0 0-228.205714 244.809143V628.297143l0.438857 6.363428a39.424 39.424 0 0 0 38.912 32.987429h33.645714l6.363429-0.512a39.424 39.424 0 0 0 32.987429-38.838857V480.768l0.658285-10.752c6.509714-67.218286 63.341714-119.808 132.388572-119.808h162.889143l7.533714-0.658286a56.246857 56.246857 0 0 0 32.548571-93.842285L817.078857 119.954286z m-392.338286 5.851428a17.042286 17.042286 0 0 0-17.042285-17.042285H201.947429l-7.753143 0.219428A136.557714 136.557714 0 0 0 65.389714 245.248v577.536l0.219429 7.753143c4.022857 71.753143 63.488 128.731429 136.338286 128.731428h620.178285l7.68-0.146285a136.557714 136.557714 0 0 0 128.804572-136.338286V613.376a17.042286 17.042286 0 0 0-17.042286-17.042286h-68.242286a17.042286 17.042286 0 0 0-17.115428 17.042286v209.408l-0.219429 4.242286a34.157714 34.157714 0 0 1-33.865143 29.915428H201.874286l-4.242286-0.292571a34.157714 34.157714 0 0 1-29.842286-33.865143V245.248l0.292572-4.242286a34.157714 34.157714 0 0 1 33.865143-29.842285h205.750857a17.042286 17.042286 0 0 0 17.042285-17.115429V125.805714z" fill="#FF5252" p-id="25743"></path></svg>
    </a>
</div>
{{#note}}
<div class="note">{{note}}</div>
{{/note}}
<br/>
{{^examples}}
<div style="font-size: 16px;">{{trans}}</div>
{{/examples}}
<div>{{examples}}</div>
<script>
    var replayButton = document.getElementsByClassName('replay-button')[0];
    if(replayButton){
        replayButton.innerHTML='<svg t="1670944272402" class="playImage" viewBox="0 0 1137 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="9821" xmlns:xlink="http://www.w3.org/1999/xlink" width="17.765625" height="16"><path d="M798.776889 282.453333a358.513778 358.513778 0 0 1 0 482.816 45.397333 45.397333 0 0 1-19.683556 23.324445 46.193778 46.193778 0 1 1-63.374222-67.015111 269.539556 269.539556 0 0 0 13.312-382.122667 47.502222 47.502222 0 0 1-22.755555-33.621333 47.160889 47.160889 0 0 1 38.912-54.101334 46.421333 46.421333 0 0 1 30.094222 5.404445c10.808889 4.949333 19.285333 14.051556 23.495111 25.315555z m161.564444-168.504889a554.325333 554.325333 0 0 1 153.031111 382.805334c0 167.082667-73.955556 316.529778-190.577777 418.588444l-0.056889-0.113778a46.364444 46.364444 0 0 1-84.878222-26.282666c0-18.261333 10.524444-34.019556 25.827555-41.642667l-0.170667-0.227555a464.384 464.384 0 0 0 159.345778-350.321778 464.042667 464.042667 0 0 0-129.308444-321.649778 47.160889 47.160889 0 1 1 66.844444-61.155556zM464.042667 33.735111C529.408-27.534222 632.035556-2.275556 632.035556 102.684444v818.232889c0 103.936-101.432889 131.527111-168.106667 68.892445l-231.992889-237.340445H90.567111c-59.505778 0-90.225778-33.564444-90.225778-90.282666V361.415111c0-57.742222 29.752889-90.282667 90.225778-90.282667h141.425778L463.985778 33.735111z m77.824 840.931556V151.722667c0-71.111111-30.378667-31.971556-61.098667-1.877334-54.158222 52.963556-135.224889 139.207111-202.126222 211.569778H150.755556c-44.828444 0-60.188444 16.270222-60.188445 60.131556v180.508444c0 44.771556 14.449778 60.131556 60.188445 60.131556h126.407111c67.299556 71.964444 149.105778 158.321778 203.320889 211.797333 31.061333 30.72 61.326222 69.006222 61.326222 0.682667z" p-id="9822"></path></svg>';
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
