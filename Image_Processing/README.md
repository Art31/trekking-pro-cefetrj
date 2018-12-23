# Image Processing

This page is a step by step description of the process of implementing and choosing algorithms and provides a summary of the scripts' motivation.

## Building the dataset

In order to perform classification or detection, 

## Algorithms studied/considered and the struggle to detect efficiently and rapidly

At first, the easiest and most practical algorithm in our roadmap to master was the sliding windows approach.

We implemented the cropping and sliding process with the help of [this tutorial from pyimagesearch](https://www.pyimagesearch.com/2015/03/23/sliding-windows-for-object-detection-with-python-and-opencv/). The next step was to find a classifier that suits our needs.

Para a escolha do classificador foram considerados modelos de SVM, regressão logística, xgboost, nearest neighbors, ensemble e redes neurais artificiais com pré-processamento. Pelo tradeoff intrínseco da velocidade e acurácia, a literatura sugeriu que o melhor seria SVM. Foi o que confirmamos na prática.

Entre todos os métodos de extração de features, os que mais se destacaram foram o HOG e o Daisy, ambos disponibilizados pelo scikit image. O link para a função de cada um se encontra abaixo.

http://scikit-image.org/docs/dev/auto_examples/features_detection/plot_daisy.html
http://scikit-image.org/docs/dev/auto_examples/features_detection/plot_hog.html

Esse link também ajuda a entender como funciona o HOG, o método mais famoso de extração de features para imagens.

https://www.learnopencv.com/histogram-of-oriented-gradients/ 

O nosso algoritmo de janela deslizante foi inspirado no tutorial do site do Adrian que se encontra abaixo. Não foram necessárias muitas modificações para fazer com que funcionasse bem para o nosso contexto.

https://www.pyimagesearch.com/2015/03/23/sliding-windows-for-object-detection-with-python-and-opencv/

Consideramos também o uso de pirâmides, através da redução de escala da imagem para que o kernel aumentasse de tamanho, e assim o algoritmo se tornaria capaz de detectar o cone em distancias diferentes. Essa tentativa em alguns contextos gerava confusão pois o cone poderia ser detectado na mesma imagem em escalas diferentes, porém parecia funcionar para certos frames, o que gerou indecisão quanto ao seu uso.

# Testes feitos em produção e resultados

Os testes realizados com os classificadores em geral indicavam bons resultados, cerca de 80% de acurácia, alguns flutuavam para 75% como SVM com kernel polinomial e regressão logística e outros chegavam a 85%, como a rede neural e o SVM com kerneis lineares e de função de base radial. Entretanto, quando usávamos um vídeo que simula o trajeto do robô, esse desempenho não se consolidava e deixava a desejar.

Com relação à parte mais relacionada à processamento de imagens, como escolha do kernel, tamanho do passo de deslocamento e superposição entre kernels vizinhos, fizemos alguns testes para identificar se havia uma melhora expressiva na performance. Novamente, essas customizações apenas faziam o algoritmo ser especialista para a nossa aplicação, algo que gostaríamos de evitar.

Os testes realizados com o método de extração daisy tiveram resultados melhores que os métodos que usaram o HOG, porém nenhum deles alcançou estabilidade no momento em que foram colocados em produção.
