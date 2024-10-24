<template>
  <div class="transition" :class="{animtrans: isActive}"></div>
  <div v-if="isShow" class="content">
    <h1>GPT신문에 오신 것을 환영합니다.</h1>
    <p>*GPT api를 활용하여, 가독성 및 정확도가 다소 부족할 수 있습니다.</p>
    <button v-if="isLoaded" @click="toggleClass" class="cta">신문 읽기</button>
    <p v-else>{{ loadingText }}</p>
  </div>
  <div v-if="!isShow" class="main">
    <h1 class="title">GPT신문</h1>
    <hr class="hr-1">
    <h2 class="summary">{{ summary }}</h2>
    <hr class="hr-1">
    <div class="move-right">
      <div ref="wordCloud" class="wordcloud"></div>
      <hr class="hr-2">
      <div class="main-content">
        <div class="word-section">
          <h3>😀</h3>
          <div ref="positiveWords" class="words-list"></div>
        </div>
        <hr class="hr-1">
        <div class="word-section">
          <h3>😢</h3>
          <div ref="negativeWords" class="words-list"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import cloud from "d3-cloud";
import * as d3 from "d3";
import axios from 'axios';

export default {
  name: "HelloWorld",
  data() {
    return {
      words: [],
      summary: "",
      positiveWords: [],
      negativeWords: [],
      isActive: false,
      isShow: true,
      isLoaded: false,
      loadingText: "로딩중...",
      loadingInterval: null,
    };
  },
  mounted() {
    this.startLoadingAnimation();
    this.fetchWordData();
  },
  beforeUnmount() {
    clearInterval(this.loadingInterval);
  },
  methods: {
    startLoadingAnimation() {
      let count = 0;
      this.loadingInterval = setInterval(() => {
        count = (count + 1) % 4;
        this.loadingText = "로딩중" + ".".repeat(count);
      }, 500);
    },
    async fetchWordData() {
      try {
        const response = await axios.get("http://203.255.92.239:10000/api/news/korean");
        if (response && response.data) {
          const { summary, positives, negatives, wordcount } = response.data;
          this.summary = summary;
          this.positiveWords = positives || [];
          this.negativeWords = negatives || [];
          this.words = Object.keys(wordcount)
            .filter(word => wordcount[word] >= 5 && wordcount[word] <= 40 && word.length > 1)
            .map(word => {
              return {
                text: word,
                size: wordcount[word] * 2,
              };
            });
          this.isLoaded = true;
        } else {
          this.loadingText = 'API 응답에 데이터가 없습니다.';
        }
      } catch (error) {
        clearInterval(this.loadingInterval);
        this.loadingText = "데이터를 불러오는 중 오류가 발생했습니다.";
      }
    },
    toggleClass() {
      if (this.isActive == true) return;
      this.isActive = true;
      setTimeout(() => {
        if (this.isLoaded){
          this.isShow = false;
          setTimeout(() => {
            this.drawWordCloud();
            this.displayWords();
          }, 1);
        }else{
          alert("failed to load content");
        }
      }, 2000);
      
    },
    drawWordCloud() {
      const width = 500;
      const height = 500;

      const layout = cloud()
        .size([width, height])
        .words(this.words)
        .padding(5)
        .rotate(() => ~~(Math.random() * 2) * 90)
        .font("Impact")
        .fontSize(d => d.size)
        .on("end", this.draw);

      layout.start();
    },
    draw(words) {
      const color = d3.scaleOrdinal(d3.schemeCategory10);

      d3.select(this.$refs.wordCloud)
        .append("svg")
        .attr("width", 500)
        .attr("height", 500)
        .append("g")
        .attr("transform", "translate(250,250)")
        .selectAll("text")
        .data(words)
        .enter()
        .append("text")
        .style("font-size", d => `${d.size}px`)
        .style("fill", (d, i) => color(i))
        .style("cursor", "pointer")
        .attr("text-anchor", "middle")
        .attr("transform", d => `translate(${[d.x, d.y]})rotate(${d.rotate})`)
        .text(d => d.text)
        .on("mouseover", function () {
          d3.select(this)
            .transition()
            .duration(200)
            .style("font-size", d => `${d.size * 1.1}px`);
        })
        .on("mouseout", function () {
          d3.select(this)
            .transition()
            .duration(200)
            .style("font-size", d => `${d.size}px`);
        });
    },
    displayWords() {
      d3.select(this.$refs.positiveWords)
        .selectAll("div")
        .data(this.positiveWords)
        .enter()
        .append("div")
        .text(d => d)
        .style("color", "green");
      d3.select(this.$refs.negativeWords)
        .selectAll("div")
        .data(this.negativeWords)
        .enter()
        .append("div")
        .text(d => d)
        .style("color", "red");
    },
  },
};
</script>

<style scoped>
* {
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}
hr {
  background-color: #eeeeee;
  padding: 0;
  margin: 10px;
}
hr.hr-1 {
  border: 0;
  height: 1px;
  background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
}
hr.hr-2 {
  border: 0;
  width: 1px;
  background-image: linear-gradient(rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
}
h3 {
  font-size: 30px;
  margin-bottom: 10px;
}
.main {
  background: #eeeeee;
  margin: 0 200px;
  transform: rotate(3deg);
}
.move-right {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
}
.main-content {
  display: grid;
  grid-template-rows: 1fr auto 1fr;
}
.wordcloud {
  width: 500px;
  height: 500px;
  margin: 0 auto;
}
.title {
  font-family: 'ClimateCrisisKR-1979';
  font-size: 72px;
  padding-top: 20px;
}
.summary {
  padding: 0 50px;
  text-align: center;
  font-size: 20px;
}
.word-section {
  margin-top: 20px;
  text-align: center;
}
.words-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}
.transition {
  position:fixed;
  height:100%;
  width:8%;
  background: #d6d6d6;
  transform: skewX(-5deg) translateX(-50px);
  transition:2s all ease-in-out;
  -webkit-transition:2s all ease-in-out;
}
.content {
  top: 40vh;
  position:relative;
  color:#000;
  z-index:10;
  height:300px;
}
.cta {
  outline:none;
  border:none;
  text-decoration:none;
  text-transform:uppercase;
  background:#202020;
  color:#eaeaea;
  box-sizing:border-box;
  margin-top:20px;
  padding:10px 40px;
}
.animtrans {
  animation: anim 4s ease-in-out;
}
@keyframes anim{
     0% { }
     20%  { z-index:11;\transform: skewX(5deg) translateX(-100%); }
     40%   { transform: skewX(0deg) translateX(0);
 width:100%; z-index:11; box-shadow: 10px 10px 5px #eaeaea;}
     60%   { transform: skewX(3deg) translateX(0);
 width:100%;z-index:11; box-shadow: 10px 10px 5px #eaeaea;}
     80%   { transform: skewX(1deg) translateX(-100%);
 width:50%;z-index:11; box-shadow: 10px 10px 5px #eaeaea;}
     100%   { transform: skewX(-5deg) translateX(-50px);
 width:8%;z-index:1; box-shadow: none;}
}
</style>
