model_css_class = '''@font-face {
  font-family: iconfont;
  src: url("_iconfont.6cad4ff.woff2");
}

:root {
    --color-grey: #dcdfe6;
    --color-grey-secondary: #8b8787;
    --color-grey-third: #acacac;
    --color-grey-fourth: #e4e4e4;
    --color-grey-fifth: #d8d8d8;
    --color-grey-sixth: #d1d1d1;
    --color-black-primary: #606266;
    --color-primary: #ff5252;
    --bg-primary: #ff3a3a;
    --border-bar: #e7e7e7;
    --color-blue-description: #46a3f4;
    --bg-switch-core-active: #ff5252;
    --bg-scrollbar: hsla(0, 0%, 67%, .5);
    --input-split: #ececec;
    --filter-icon: invert(0);
}

body {
    --content-color: #3a3a3a;
    --color: #3d454c;
    --color-desc: #8b8787;
    --color-secondary: #5a5e66;
    --bg: #f8f8f8;
    --bg-secondary: #fff;
    --bg-third: #f1f1f1;
    --bg-fourth: #fff;
    --bg-fifth: #fff5f5;
    --bg-sixth: #d8d8d8;
    --bg-seventh: #f8f8f8;
    --bg-icon: #e4e4e4;
    --bg-hover-primary: #ff3a3a;
    --border-color: #dcdfe6;
    --border-color-primary: #ffcbcb;
    --border-color-secondary: #ffb7b7;
    --border-color-third: #ececec;
    --btn-border: #ffcbcb;
    --btn-primary-secondary: #ffd8d8;
    --btn-color: #ff3a3a;
    --btn-bg: #fff5f5;
    --folder: #ffe88c;
    --border: #ececec;
    --hr: #d8d8d8;
    --bg-input: #f9f9f9;
    --border-input: #dfdfdf;
    --hover-color: rgba(0, 0, 0, .04);
    --border-btn-basic: #ff3a3a;
    --color-slider: #ececec;
    --bg-tag: rgba(0, 0, 0, .04);
    --bg-card-hover: #fff;
    --bg-image: #ececec;
    --search-input-border: #3b3b3b;
    --boxshadow-search: #ececec;
    --bg-search-input: #fff;
    --bg-setting-card: #fff;
    --bg-slider: #f8f8f8;
    --bg-slider-active: #fff;
    --bg-switch: #f8f8f8;
    --bg-switch-core: #ececec;
    --border-tag: #acacac;
    --bg-article-translation: rgba(0, 0, 0, .02);
    --content-hover-bg: #ffcbcb;
    --bg-radio: #ff5252;
    --radio-color: #fff;
    --bg-chunk-yellow: #fae6b8;
    --bg-chunk-blue: #ececec;
    --bg-chunk-gray: #ececec;
    --bg-chunk-orange: #fae6b8;
    --border-chunk-color-gray: #ccc;
    --border-chunk-color-orange: #ffc84a;
    --content-color-analysis: #3a3a3a;
    --color-gray: #8b8787;
    --bg-radio-second: #1c1c1e;
}

body.nightMode {
    --content-color: #fafafa;
    --color-secondary: #fafafa;
    --color: #fff;
    --color-desc: #565656;
    --color-secondary: #fff;
    --bg: #0e0e11;
    --bg-secondary: #3d454c;
    --bg-third: #3b3b3b;
    --bg-fourth: #1c1c1e;
    --bg-fifth: #63474c;
    --bg-sixth: #3d343c;
    --bg-seventh: #1c1c1e;
    --bg-icon: #5c6369;
    --bg-hover-primary: #ff3a3a;
    --border-color: #dcdfe6;
    --border-color-primary: #ffcbcb;
    --border-color-secondary: #ff3a3a;
    --border-color-third: #3b3b3b;
    --btn-border: #565656;
    --btn-primary-secondary: #4d3038;
    --btn-color: #8b8787;
    --btn-bg: #4d343c;
    --border: #3b3b3b;
    --hr: #565656;
    --folder: #3d454c;
    --bg-input: #1c1c1e;
    --border-input: #565656;
    --border-bar: #565656;
    --hover-color: hsla(0, 0%, 100%, .08);
    --border-btn-basic: #f1f1f1;
    --color-slider: #565656;
    --bg-tag: hsla(0, 0%, 100%, .1);
    --bg-card-hover: #2b3a47;
    --bg-image: #3d454c;
    --color-sidebar: #757470;
    --search-input-border: #ececec;
    --boxshadow-search: #3b3b3b;
    --bg-search-input: #1c1c1e;
    --bg-setting-card: #1c1c1e;
    --bg-slider: #0e0e11;
    --bg-slider-active: #1c1c1e;
    --bg-switch: #0e0e11;
    --bg-switch-core: #3b3b3b;
    --border-tag: #565656;
    --bg-article-translation: hsla(0, 0%, 100%, .08);
    --content-hover-bg: #ff3a3a;
    --bg-radio: #1c1c1e;
    --radio-color: #ff3a3a;
    --filter-icon: invert(1);
    --bg-chunk-yellow: #44381c;
    --bg-chunk-blue: #3b3b3b;
    --bg-chunk-gray: #3b3b3b;
    --bg-chunk-orange: #44381c;
    --border-chunk-color-gray: #555;
    --border-chunk-color-orange: #6c5b33;
    --content-color-analysis: #fafafa;
    --color-gray: #acacac;
    --bg-radio-second: #fff;
}

.iconfont {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    font-family: iconfont !important;
    font-size: 20px;
    font-style: normal;
}

a {
    text-decoration: none;
}

* {
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
}

body {
    box-sizing: border-box;
    background-color: var(--bg);
    color: var(--color);
    transition: background-color .3s;
    height: fit-content;
    outline: none;
    padding: 0 16px;
    position: relative;
    width: 100%;
    font-display: swap;
    font-family: -apple-system, BlinkMacSystemFont, Helvetica Neue, PingFang SC, Microsoft YaHei, Source Han Sans SC, Noto Sans CJK SC, WenQuanYi Micro Hei, sans-serif;
    margin: 0;
    overflow-x: hidden;
}

.android body {
    padding: 0 9px;
}

.ios body, .ipad body {
    text-align: start;
}

body.nightMode {
    background-color: var(--bg);
    color: var(--color);
}

.ZH_S, .ZH_S .font-main, .ZH_S .font-main-middle {
    font-family: -apple-system, PingFangSC-Regular, AlibabaPuHuiTi, Microsoft Yahei, 黑体, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif;
}

.ZH_S .font-JP {
    font-family: Hiragino Kaku Gothic Pro, PingFangSC-Regular, AlibabaSansJP, AlibabaPuHuiTi, Meiryo, Tahoma, Arial, Microsoft Yahei, 黑体;
}

*, :after, :before {
    box-sizing: border-box;
    margin: 0;
}

.word-head {
    background-color: var(--bg);
    box-sizing: border-box;
    padding: 20px 16px 0;
    position: sticky;
    top: 0;
    z-index: 2;
}

.android .word-head {
    padding: 0
}

.spell {
    color: var(--color);
    font-family: Hiragino Mincho ProN, Hiragino Kaku Gothic Pro, PingFangSC-Regular, AlibabaSansJP, AlibabaPuHuiTi, Meiryo, Tahoma, Arial, Microsoft Yahei, 黑体;
    font-size: 36px;
    font-weight: 600;
    line-height: 1.2;
    margin: 0 0 6px;
    position: relative;
    text-align: justify;
    width: 100%;
    z-index: 3;
}

.accent {
    font-size: 14px;
    line-height: 18px;
    margin-left: 4px;
    position: absolute;
}

.head-sub {
    align-items: center;
    display: flex;
    flex-direction: row;
    font-size: 16px;
    justify-content: flex-start;
    line-height: 20px;
    margin-bottom: 16px;
    margin-top: 10px;
}

.entry-voice-container {
    height: 20px;
    margin-left: 12px;
    margin-right: 16px;
    width: 20px;
}

.voice-container, .replay-button {
    cursor: pointer;
    display: inline-block;
    height: 20px;
    line-height: 20px;
    outline: none;
    position: relative;
    width: 20px;
}

.iconic-common-voice {
    color: var(--color-primary);
}
.mobile .word-voice {
    margin-left: auto;
}
.mobile .iconic-common-voice {
    font-size: 30px;
}

.iconic-common-voice:before {
    content: "\e6c6";
}

.word-tool {
    align-items: center;
    display: flex;
    flex-direction: row;
    font-size: 16px;
    justify-content: flex-start;
    line-height: 20px;
    padding: 10px 0 16px;
}


.word-speech {
    font-size: 14px;
    line-height: 18px;
    position: relative;
    white-space: nowrap;
    z-index: 0;
}

.word-speech:before {
    background-color: var(--color-word-tag-underline);
    border-radius: 4px;
    bottom: 0;
    content: "";
    height: 4px;
    left: -2px;
    position: absolute;
    right: -2px;
    z-index: -1;
}

.split—line {
    background: var(--color-grey-third);
    height: 12px;
    margin: 0 12px;
    width: .5px;
}

.word-tag {
    background: hsla(0, 0%, 67%, .1);
    border-radius: 12px;
    color: var(--color-gray);
    font-size: 11px;
    line-height: 14px;
    padding: 5px 12px;
    white-space: nowrap;
}

.icon-wrap {
    cursor: pointer;
    margin-right: 12px;
}

.to-moji .iconfont, .update-word .iconfont {
    color: var(--content-color);
    font-size: 20px;
}

.to-moji i:before{
    content: "\e6c7"
}

.update-word i:before{
    content: "\e6a7"
}

.word-detail>div:first-child {
    margin-top: 36px;
}

.word-detail>div:not(:first-child) {
    margin-top: 24px;
    padding-bottom: 16px;
}

.paraphrase .paraphrase-header {
    align-items: center;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    margin-bottom: 16px;
    position: relative;
}

.paraphrase .paraphrase-header .title {
    font-family: PingFangSC-Medium, AlibabaPuHuiTi, Microsoft Yahei, 黑体, BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Ubuntu, Cantarell, Open Sans, Helvetica Neue, sans-serif;
    font-size: 16px;
    line-height: 20px;
}

.paraphrase .paraphrase-header .btn-fold {
    cursor: pointer;
    position: absolute;
    right: 21px;
    top: 2px;
}

.iconic_toolbar_hide:before {
    content: "\e613";
}

.paraphrase .subdetail_header {
    align-items: center;
    background-color: hsla(0, 0%, 67%, .1);
    border: none;
    border-radius: 12px;
    color: var(--color);
    cursor: pointer;
    display: flex;
    flex-direction: row;
    font-size: 16px;
    font-weight: 500;
    height: auto;
    justify-content: center;
    line-height: 20px;
    margin-bottom: 16px;
    position: relative;
}

.subdetail-container {
    cursor: auto;
    font-weight: 400;
    line-height: 1.6;
    padding: 4px 0 12px 16px;
    position: relative;
    text-align: justify;
    width: 100%;
}

.column {
    color: var(--content-color);
    display: flex;
    margin-top: 8px;
}

.column .icon {
    height: 24px;
    min-width: 20px;
    width: 20px;
}

.column .label {
    margin-left: 8px;
}

.column .icon_continue {
    height: 20px;
    margin-top: 12px;
    width: 34px;
}

.column .icon_context {
    height: 20px;
    margin-top: 12px;
    width: 57px;
}

.paraphrase .subdetail_header .subdetail_icon_wrap {
    padding: 0 16px;
}

.paraphrase .subdetail_header .subdetail_icon.is-active {
    transform: rotate(90deg);
}

.paraphrase .subdetail_header .subdetail_icon {
    speak: none;
    font-feature-settings: normal;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    display: inline-block;
    font-style: normal;
    font-variant: normal;
    line-height: 1;
    text-transform: none;
    vertical-align: baseline;
    background: hsla(0, 0%, 67%, .1);
    border-radius: 10px;
    color: #979797;
    font-size: 12px;
    font-weight: 800;
    padding: 4px;
    -webkit-user-select: none;
    -moz-user-select: none;
    user-select: none;
}

.icon-arrow-right:before {
    content: "\e631";
}

.paraphrase .examplesContainer {
    max-height: 0;
    overflow: hidden;
    position: relative;
    transition: all .3s ease-in-out;
}

.paraphrase .examplesContainer.active {
    animation: overVisible 0s ease-out .4s forwards;
    max-height: calc(var(--exampleNum)* 500px);
}

.paraphrase .subdetail_header .noneChildren+.subdetail_icon_wrap {
    opacity: 0;
}

.paraphrase .subdetail_container:last-child .example-details .example-inner:last-child {
    margin-bottom: 16px;
}

.example-inner {
    align-items: center;
    box-sizing: border-box;
    display: flex;
    margin-bottom: 24px;
    padding-left: 16px;
}

.example-inner .example-info {
    display: flex;
    flex-direction: column;
    margin-right: 24px;
}

.example-inner .example-info .line1 {
    color: var(--content-color);
    font-size: 16px;
    font-weight: 500;
    line-height: 20px;
}

.example-inner .example-info .line2 {
    color: var(--color-grey-secondary);
    font-size: 14px;
    font-weight: 400;
    line-height: 18px;
    margin-top: 2px;
    white-space: pre-line;
}

.hidden {
    display: none;
}

.note-header, .conjunctive-header {
    align-items: center;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    padding-bottom: 16px;
    position: relative;
}

.note-body {
    border: 1px solid;
    border: 1px solid var(--color-grey-third);
    border-radius: 12px 12px 12px 12px;
    opacity: 1;
    padding: 12px 16px;
}

.conjunctive-body {
    border-bottom: .5px solid var(--color-grey-third);
    border-top: .5px solid var(--color-grey-third);
}



ruby rt {
    ruby-align: distribute-space;
    color: var(--color-grey-secondary) !important;
    font-size: .7rem !important;
    font-weight: 400;
    text-align: center;
    transform: scale(.9) translateY(-2px);
    -webkit-user-select: none;
    -moz-user-select: none;
    user-select: none;
}

ruby rt:before {
    content: attr(hiragana);
}'''

front_pron = '''<div class="word-head">
    <div class="head-spell">
        <span class="spell">{{pron}}{{accent}}</span>
    </div>
    <div class="head-sub">
        <div class="entry-voice-container word-voice">
            {{sound}}
        </div>
    </div>
</div>
<script>
    if (document.documentElement.classList.contains('android')) {
        replayButtonClassName = 'replaybutton'
    } else {
        replayButtonClassName = 'replay-button'
    }
    replayButton = document.querySelector('.' + replayButtonClassName);
    if(replayButton){
        replayButton.innerHTML='<i class="iconfont iconic-common-voice"></i>';
    }
</script>
'''

front_spell = '''<div class="word-head">
    <div class="head-spell">
        <span class="spell">{{spell}}</span>
    </div>
</div>'''

front_trans = '''<div class="word-head">
    <div class="word-tool">
        {{part_of_speech}}
    </div>
</div>
<div class="word-detail">
    <div class="paraphrase">{{trans}}{{^trans}}{{excerpt}}{{/trans}}</div>
</div>'''

detail = '''<script>
    // 初始是否展开所有例句，选填 true 或 false
    initAllActive = true
    
    // 是否显示罗马音，选填 true 或 false
    showRomaji = false
    
    // 是否显示音调符号，选填 true 或 false
    showAccent = true
    
    // 是否显示分级标签，选填 true 或 false
    showTag = true
    
    // 活用型版本A(五段/一段/カ变/サ变)或B(一类/二类/三类)，选填 'A' 或 'B'
    katuyouVersion = 'A'
    
    // 释义/详解(1)、笔记(2)的显示顺序，选填 "12" 或 "21"
    showOrder = "21"
</script>

<div class="word-head">
    <div class="head-spell">
        <span class="spell">{{spell}}</span>
        <span class="accent">{{accent}}</span>
    </div>
    <div class="head-sub">
        <div class="pron">{{pron}}</div>
        <div class="split—line romaji-split hidden"></div>
        <div class="romaji hidden"></div>
        <div class="entry-voice-container word-voice">
            {{sound}}
        </div>
    </div>
    <div class="word-tool">
        {{part_of_speech}}
        {{#part_of_speech}}
        <div class="split—line"></div>
        {{/part_of_speech}}
        <div class="word-tag hidden"></div>
        <div class="split—line tag-split hidden"></div>
        <div class="el-tooltip icon-wrap item">
            <a class="to-moji" href="{{MojiToAnki_link:link}}">
                <i class="iconfont iconic-common-share"></i>
            </a>
        </div>
        <div class="el-tooltip icon-wrap item">
            <a class="update-word" onclick="pycmd('MojiToAnki_update')" href="#">
                <i class="iconfont"></i>
            </a>
        </div>
    </div>
</div>

<div class="word-detail">
    <div class="note">
    {{#note}}
        <div class="note-header">
            <span class="title">笔记</span>
        </div>
        <div class="note-body">
            <div class="note-content">{{note}}</div>
        </div>
    {{/note}}
    </div>

    {{examples}}
    
    {{^examples}}
    <div class="paraphrase">{{trans}}{{^trans}}{{excerpt}}{{/trans}}</div>
    {{/examples}}
</div>

<script>
    if (document.documentElement.classList.contains('android')) {
        replayButtonClassName = 'replaybutton'
    } else {
        replayButtonClassName = 'replay-button'
    }
    replayButton = document.querySelector('.' + replayButtonClassName);
    if(replayButton){
        replayButton.innerHTML='<i class="iconfont iconic-common-voice"></i>';
    }
</script>
<script>
    subdetailHeaders = document.getElementsByClassName('subdetail_header')
    for (let subdetailHeader of subdetailHeaders) {
        subdetailHeader.isActive = () =>  subdetailHeader.nextElementSibling.classList.contains('active')
        subdetailHeader.setActive = newValue => {
            if(newValue) {
                subdetailHeader.nextElementSibling.classList.add('active')
                subdetailHeader.getElementsByClassName('subdetail_icon')[0].classList.add('is-active')
            } else {
                subdetailHeader.nextElementSibling.classList.remove('active')
                subdetailHeader.getElementsByClassName('subdetail_icon')[0].classList.remove('is-active')
            }
        }
        subdetailHeader.onclick = () => {
            subdetailHeader.setActive(!subdetailHeader.isActive())
        }
    }
    
    subdetailHeadersArray = Array.from(subdetailHeaders)
    btnFoldDom = document.querySelector('.btn-fold')
    if (btnFoldDom) {
        btnFoldDom.onclick = () => {
            isAllNotActive = subdetailHeadersArray.reduce((accumulator, subdetailHeader) => accumulator && !subdetailHeader.isActive(), true)
            subdetailHeadersArray.forEach(subdetailHeader => subdetailHeader.setActive(isAllNotActive))
    }
    }
</script>
<script>
    if (initAllActive) {
        subdetailHeadersArray.forEach(subdetailHeader => subdetailHeader.setActive(true))
    }
    
    wordSpeechDom = document.querySelector('.word-speech')
    if (wordSpeechDom) {
        wordSpeechDom.innerHTML = wordSpeechDom.getAttribute(katuyouVersion && katuyouVersion === 'B' ? 'b' : 'a')
    }
    
    if (!showAccent) {
        const accentDom = document.querySelector('.accent')
        if (accentDom) {
            accentDom.style.display = 'none'
        }
    }
    
    pronDom = document.querySelector('.pron>span')
    if (pronDom) {
        const pron = pronDom.getAttribute('pron')
        const romaji = pronDom.getAttribute('romaji')
        const spell = document.querySelector('.spell').getInnerHTML()
        if (pron === spell) pronDom.style.display = 'none'
        if (showRomaji && romaji) {
            if (pron && pron !== spell) {
                document.querySelector('.romaji-split').classList.remove('hidden')
            }
            const romajiDom = document.querySelector('.romaji')
            romajiDom.innerHTML = romaji
            romajiDom.classList.remove('hidden')
        }
        if (showTag) {
            const tag = pronDom.getAttribute('tag')
            if (tag) {
                document.querySelector('.tag-split').classList.remove('hidden')
                const tagDom = document.querySelector('.word-tag')
                tagDom.innerHTML = tag
                tagDom.classList.remove('hidden')
            }
        }
    }
    
    wordDetailDom = document.querySelector('.word-detail')
    if (wordDetailDom) {
        const showOrderList = Array.from((showOrder || "12") + "3")
        const showClassNameMap = {"1": "paraphrase", "2": "note", "3": "conjunctive"}
        orderedChildDomList = showOrderList.map(index => document.querySelector('.' + showClassNameMap[index]))
        wordDetailDom.innerHTML = ''
        for (let child of orderedChildDomList) {
            if (child) wordDetailDom.appendChild(child)
        }
    }
</script>'''
