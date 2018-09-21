<h1>Contador de veículos</h1>
<h2>Objetivo</h2>
<p>Realizar a contagem de veículos sem a utilização de sensores ou qualquer hardware que não seja próprio para captação de vídeos (cameras).</p>
<h2>Motivação</h2>
<p>A motivação para o desenvolvimento desse projeto foi, principalmente, o aprendizado da tecnologia de inteligência artificial conhecida como Deep Learing, que é uma variação dos algoritmos de redes neurais.</p>
<p>A contagem de veículos foi escolhida porque através dela é também possível validar a utilização do reconhecimento de objetos através das redes neurais profundas para outras atividades como por exemplo:</p>
<ul>
<li>Contagem de pessoas</li>
<li>Reconhecimento de pessoas em áreas de risco como fábricas e canteiros de obra</li>
<li>Movimentação de veículos em áreas não permitidas</li>
<li>Acionamento de travas de segurança conforme o número de pessoas ou objetos reconhecidos</li>
</ul>
<h2>Desenvolvimento</h2>
<p>Todo o desenvolvimento foi feito em python utilizando o framework para deep learning TensorFlow.</p>
<p>Para esse experimento não foi criado nenhum modelo, foi utilizado ssd_mobilenet_v1_coco_2017 (mais informações podem ser encontradas aqui <a hre="https://github.com/tensorflow/models/tree/master/research/object_detection">github da API de detecção de objetos</a>.</p>
<p>Para aumentar a acuracia e a velocidade o modelo foi retreinado utilizando-se somente uma classe (carro).</p>
