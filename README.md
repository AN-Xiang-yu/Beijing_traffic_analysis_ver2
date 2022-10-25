<h1>Beijing_traffic_analysis</h1> 

Here is the link to run our project
https://an-xiang-yu-beijing-traffic-analysis-ver2-app-ulo4b0.streamlitapp.com/

<article> 
  <section>
    <h2>Table of contents </h2>
    <nav>
      <ol>
        <li><a href = "#introduction">Introduction</a></li>
        <li><a href = "#installation">Installation and execution at local</a></li>
        <li><a href = "#processing">Processing the data</a></li>
        <li><a href = "#contributors">Contributors -- Group 6 of DAI</a></li>
      </ol>
    </nav>
  </section>
</article>

<article>
  <section id="introduction">
    <h2>1. Introduction</h2>
    <div> 
      <p>
        Due to the high density of cars on the streets on the city of Beijing, China, which is leading to large traffic congestions especially in large cities, the city has decided to run analysis on the daily commute of transportation vehicles, namely taxi cars. By analyzing the commute of taxi drivers. Through this analysis, we can get an estimate of how long it takes an individual to get from one point to another, and what are the points of highest traffic.  
      </p>
      <p>
      In this project, we create a Streamlit application, we use github as our server to run this application, users can use this application to check the cab congestion in Beijing, the shortest distance from one point to another, the time taken and the time and cost. Finally, users can view the density of cabs and cars in Beijing at different times of the day and compare it to some other major cities in the world.
      </p>
    </div>
  </section>
</article>

<article>
  <section id="Installation">
    <h2>2. Installation and execution at local</h2>
    <div> 
      <p>
        If you want to reproduce our project in your computer:<br>
        1) You should have download <a href="https://streamlit.io/"><b>steamlit</b></a>, <a href="https://www.python.org/downloads/"> <b>python</b> </a> and <a href="https://www.anaconda.com/products/distribution"> <b>anaconda</b> </a> in your computer. <br>
        2) And then you can download our projet. <br>
        3) You should then use the cmd.exe and move to the folder where the project app.py is located. <br>
        4) Type streamlit run app.py and your project will run normally. <br>
      </p>
    </div>
  </section>
</article>

<article>
  <section id="processing">
    <h2>3. Processing the data</h2>
    <div> 
      <p>
        If you want to regenerate the data, you first need to download the dataset of <a href="https://www.microsoft.com/en-us/research/publication/t-drive-trajectory-data-sample/"><b>taxi_log_2008_by_id</b></a>
      </p>
    </div>
    <div> 
      <h3>For the best route from point A to point B and the most crowded street function </h3>
      <p>
        1) Since we are using the Beijing Road Network file, we need to first use coordTrans.py to transform all the coordinates, separate the data and store it in the csv/segment folder.<br>
        2) Next, you need to use clustering.py to process all the files in csv/segment and store them in the csv/cluster file.<br>
        3) And then you need to use create_map.py to process all the files in map/cluster, put all the points on the road network, and put the newly generated files in csv/map.<br>
      </p>
    </div>
    <div> 
      <h3>For the Average car density of Beijing function </h3>
      <p>
        1) You need to use density_data_process.py for processing.<br>
        2) After running the density_data_process.py file, the taxi_data.csv file will be generated in the csv folder.<br>
      </p>
    </div>
  </section>
</article>

<article> 
  <section id="contributors">
    <h2>4. contributors -- Group 6 of DAI </h2>
    <div> 
      <p><a href = "https://www.linkedin.com/in/xiangyu-an-34109a196/"><b>AN, Xiangyu </b></a> </p>
      <p><a href = "https://www.linkedin.com/in/m%C3%A9lisande-gr%C3%A9goire-b%C3%A9granger-a5654219b/"><b>GRÉGOIRE--BÉGRANGER Mélisande</b></a> </p>
      <p><a href = "https://www.linkedin.com/in/sugitha-nadarajah-07681119b/"><b>NADARAJAH Sugitha</b></a></p>
    </div>
  </section>
</article>

