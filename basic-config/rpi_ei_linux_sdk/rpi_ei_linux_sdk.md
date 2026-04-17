# Instalação de Bibliotecas Python para o RPi
Nesse roteiro de laboratório você instalará bibliotecas python para o seu RPi incluindo Edge Impulse Linux Python *SDK*, Pyserial, Matplotlib, TFlite, Opencv, Jupyter Notebook e VSCode.

## Visão Geral das Bibliotecas
[Edge Impulse Linux Python *SDK*](https://github.com/edgeimpulse/linux-sdk-python) permite executar modelos de aprendizado de máquina e coletar dados de sensores em máquinas Linux usando Python.

[PySerial](https://pyserial.readthedocs.io/en/latest/)  é uma biblioteca Python que encapsula o acesso à porta serial, facilitando a comunicação com dispositivos conectados via interfaces seriais, como USB. Ele é amplamente utilizado em projetos de automação, robótica e Internet das Coisas (IoT) para enviar e receber dados de sensores, microcontroladores e outros dispositivos seriais.


[OpenCV](https://opencv.org/), uma biblioteca de visão computacional amplamente utilizada para processamento de imagens e vídeos.

[Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/stable/) e [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/) são ferramentas poderosas para desenvolvimento interativo em Python, permitindo criar e compartilhar documentos que contêm código executável, visualizações e texto explicativo.

[VSCode (Visual Studio Code)](https://code.visualstudio.com/docs) é um editor de código-fonte leve, mas poderoso, que pode ser usado remotamente para editar código em um Raspberry Pi.

## Requisitos
- Configure seu RPi conforme descrito no roteiro de laboratório [Configurações iniciais do RPi](../rpi_basic_config/rpi_basic_config.md)
- Instale as ferramentas CLI e do SDK do Edge Impulse conforme o roteiro de laboratório [Instalação do Edge Impulse Linux CLI](../rpi_ei_linux/rpi_ei_linux.md)
<!--- Assegure-se de que estejam instalados o `python3-pip`, `python3-venv` e `python3-picamera2`:
    - O `python3-pip` é o gerenciador de pacotes oficial para Python 3, permitindo instalar e gerenciar bibliotecas e dependências de forma simples. 
    - o `python3-venv` é um módulo que permite criar ambientes virtuais isolados para projetos Python, facilitando a gestão de dependências específicas sem afetar o sistema global.
        ```bash
        sudo apt install -y python3-pip python3-venv    
        ```
-->        
- Certifique de que o RPI tem Python 3 (>=3.7) instalado.
    - **Conecte-se ao RPi via SSH** ou abra um terminal diretamente nele.
    - Então, no terminal no seu RPi e digite um dos seguintes comandos:
    ```bash
        python3 --version
    ```
    Ou sua forma abreviada.
    ```bash
        python3 -V
    ```
    Pressione `Enter` e a saída será algo como
    ```bash
        Python 3.9.2
    ```
    Se o número da versão exibido for `3.7.0` ou superior (como `3.8.x`, `3.9.x`, etc.), então a versão do python atende ao requisito.

    Instalação do `pip`
    ```bash
    sudo apt update
    sudo apt install python3-pip
    ```

## Bibliotecas em Nível de Sistema
### Bibliotecas para Câmera no RPi
- Não podem faltar no seu RPi o [`libcamera`](https://www.raspberrypi.com/documentation/computers/camera_software.html) e o [`picamera2`](https://github.com/raspberrypi/picamera2).
- No entanto, essas biliotecas **não precisam ser instaladas** pois já são padrão nas versões recentes do Raspberry Pi OS. Consulte a [documentação oficial do libcamera](https://www.raspberrypi.com/documentation/computers/camera_software.html) e a [documentação do picamera2](https://github.com/raspberrypi/picamera2) para mais detalhes.
    A principal diferença entre os dois reside na sua posição na arquitetura de software da câmera do Raspberry Pi:
    - `libcamera` é a infraestrutura de baixo nível (o *backend*)
    - `picamera2` é uma biblioteca Python de alto nível (o *frontend*) que facilita o uso da câmera.

- Pense neles da seguinte forma:
    - `libcamera` é o motor de um carro: a parte complexa, poderosa e fundamental que faz tudo funcionar.
    - `picamera2` é o volante e os pedais: a interface simples que você usa para controlar o motor sem precisar entender de mecânica.

    Quando você escreve um código em Python para controlar a câmera do seu Raspberry Pi, você sempre usará a picamera2. Você não precisa se preocupar com os detalhes internos da libcamera.

- Aqui está um detalhamento mais aprofundado:
    - **libcamera**
        * **O que é?** Uma estrutura de câmera de código aberto para Linux. No Raspberry Pi, ela substituiu a antiga pilha de câmera de código fechado.  
        * **Nível:** **Baixo Nível**. Ela lida com a complexidade de acessar o hardware da câmera, processar os dados brutos do sensor e expor controles detalhados.  
        * **Linguagem:** É escrita principalmente em C++.  
        * **Uso:** Você não interage diretamente com a libcamera em seu código Python. Ela funciona nos bastidores do sistema operacional. Desenvolvedores avançados ou aplicativos do sistema (como as ferramentas de linha de comando libcamera-still e libcamera-vid) a utilizam diretamente.

    - **picamera2**
        * **O que é?** A biblioteca Python oficial e recomendada para controlar câmeras no Raspberry Pi que usam o sistema operacional "Bullseye" ou mais recente.  
        * **Nível:** **Alto Nível**. Ela oferece uma API simples e intuitiva para tarefas comuns como tirar fotos, gravar vídeos e ajustar configurações (resolução, taxa de quadros, etc.).  
        * **Linguagem:** É escrita em Python.  
        * **Uso:** Esta é a biblioteca que você **importa e usa em seus scripts Python**. Cada comando que você dá na picamera2 (como picam2.start\_and\_capture\_file()) é traduzido por ela em instruções mais complexas para a libcamera.
- Tabela Comparativa

    | Característica | libcamera | picamera2 |
    | :---- | :---- | :---- |
    | **Função** | Infraestrutura de sistema (Backend) | Biblioteca de aplicação (Frontend) |
    | **Nível de Abstração** | Baixo Nível | Alto Nível |
    | **Linguagem Principal** | C++ | Python |
    | **Público-Alvo** | Desenvolvedores do sistema operacional | Desenvolvedores de aplicações Python |
    | **Relação** | É a base sobre a qual a picamera2 opera. | Fornece uma interface amigável para a libcamera. |

- Resumindo:
    - Quando você escreve um código em Python para controlar a câmera do seu Raspberry Pi, você sempre usará a `picamera2`. Você não precisa se preocupar com os detalhes internos da `libcamera`, apenas precisa garantir que ela esteja instalada no seu sistema operacional (o que já é padrão nas versões recentes do Raspberry Pi OS).
### Instalação do Edge Impulse Linux Python *SDK*
No terminal do RPi instale o [Edge Impulse Linux Python *SDK*](https://docs.edgeimpulse.com/tools/libraries/sdks/inference/linux/python), executando os seguintes comandos:
```bash
sudo apt-get install libatlas-base-dev libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
pip3 install edge_impulse_linux -i https://pypi.python.org/simple
pip3 install pyaudio
```
### Instalação do Pyserial
 Para ter o Pyserial completamente funcional, precisamos:.
- Passo 1: Instalar o PySerial

    Para instalar o PySerial, execute o seguinte comando no terminal do RPi:
    ```bash
    pip3 install pyserial
    ```
- Passo 2: Configurar permissões

    Por padrão no Raspberry Pi OS, o usuário `pi` (ou o seu usuário padrão) pode não ter permissão para acessar as portas seriais, o que causaria um erro de `Permission denied`.
    Para resolver isso, adicione seu usuário ao grupo dialout:
    ```bash
    sudo usermod -a -G dialout $USER
    ```
    Depois de executar esse comando, é necessário reiniciar o RPi para que as alterações tenham efeito:
    ```bash
    sudo reboot
    ```

### Configuração do Driver de Áudio (Device Tree)
O INMP441 não possui driver nativo "plug-and-play". Utilizamos o overlay do Google VoiceHAT para compatibilidade.
Edite o arquivo de boot:
```bash
sudo nano /boot/firmware/config.txt
```
A localização desse arquivo pode ser /boot/config.txt em versões antigas.

Adicione ao final do arquivo:
```bash
Ini, TOML
## Habilita suporte a Audio I2S genérico
dtparam=i2s=on
# Carregar o driver de som compatível com o INMP441
dtoverlay=googlevoicehat-soundcard
```
Reinicie o dispositivo:
```bash
sudo reboot
```
### Instalação de Dependências de Software
Instalação das bibliotecas de sistema e pacotes Python necessários para a coleta multimodal.
```bash
sudo apt-get update
```
Ferramentas de compilação e bibliotecas de áudio:
```bash
sudo apt-get install -y python3-pip python3-pyaudio portaudio19-dev libatlas-base-dev i2c-tools git
```
Bibliotecas Python do projeto
```bash
sudo pip3 install pyaudio requests smbus bme680 luma.oled adafruit-circuitpython-ssd1306 pillow
```


### Instalação do **OpencV**
Instalar o OpenCV em um Raspberry Pi 3B pode ser um processo demorado, no entanto, é um passo fundamental para projetos de visão computacional.

A instalação pode ser feita de duas maneiras principais:
- usando o gerenciador de pacotes `apt` ou
- compilando a partir do código-fonte.

A seguir, detalho o método usando pacotes `apt`, o qual recomendo para a maioria dos usuários devido à sua simplicidade e rapidez.
> Se decidir compilar a partir do código-fonte, esteja ciente de que o processo pode ser demorado (pode levar de 6 a 12 horas no RPi 3B), complexo  e propenso a erros. A compilação a partir do código-fonte só é recomendada se você precisar de uma funcionalidade muito específica que não está disponível nos pacotes padrão.

Abaixo, você tem um guia completo com o método mais recomendado e atualizado: vamos usar pacotes que agilizam o processo e evitam a compilação completa, que pode levar muitas horas.

#### Instalação Automatizada do OpenCV
Utilizaremos um script para automatizar a instalação. Se preferir instalar manualmente pule para a próxima a seção "Instalação manual do OpenCV"

* Agora que vocês está conectado ao RPi por SSH:
  1. Faça o download do seguinte script:
    ```bash
     wget https://raw.githubusercontent.com/fabiobento/sis-emb-2025-2/refs/heads/main/aulas/sbc-rpi/rpi_ei_linux_sdk/scripts/install_rpi_opencv.sh
    ```    
  2. No mesmo diretório em que baixou o script acima, conceda permissão de execução:
    ```bash
    chmod +x install_rpi_opencv.sh
    ```
  3. Agora execute o script:
    ```bash
    ./install_rpi_opencv.sh

#### Instalação manual do OpenCV
Se preferir instalar o OpenCV manualmente, siga os passos abaixo:
- **Passo 1**: Preparar o RPi
    - Primeiro, é importante garantir que seu sistema operacional e firmware estejam totalmente atualizados. Abra o terminal em seu computador pessoal, reestabeleça a comunicação SSH com o RPi. Depois execute os seguintes comandos:
        ```bash
        sudo apt update -y
        ```
    - Em seguida, reinicie o RPi para garantir que todas as atualizações sejam aplicadas:
        ```bash
        sudo reboot
        ```

- **Passo 2**: Aumentar o espaço de Swap
    - A compilação ou instalação de pacotes pesados como o OpenCV pode consumir muita memória RAM. O RPi 3B tem apenas 1 GB de RAM, o que pode causar travamentos. Para evitar isso, vamos aumentar temporariamente o tamanho do arquivo de troca (swap), que funciona como uma "RAM virtual":
    1. Abra o arquivo de configuração de swap:
        ```bash
        sudo nano /etc/dphys-swapfile
        ```
    2. Altere o tamanho do swap. Procure pela linha `CONF_SWAPSIZE=100` e altere o valor para 2048 (ou seja, 2 GB).
        ```bash
        # set size to absolute value, leaving empty (default) then uses computed value
        #   you most likely don't want this, unless you have an special disk situation
        # CONF_SWAPSIZE=100
        CONF_SWAPSIZE=2048
        ```
    3. Salve e saia: Pressione `Ctrl+X`, depois `Y` e `Enter`.
    4. Aplique as alterações reiniciando o serviço de swap:
        ```bash
        sudo /etc/init.d/dphys-swapfile restart
        ```
- **Passo 3**: Instalar o OpenCV e suas dependências
    - Ainda bem que as versões mais recentes do Raspberry Pi OS incluem pacotes pré-compilados para o OpenCV nos seus repositórios, o que torna a instalação muito mais rápida do que compilar do zero.

    1. Instale as bibliotecas principais do OpenCV e os pacotes Python:
        ```bash
        sudo apt install python3-opencv -y
        ```
    2. Para garantir que o OpenCV possa ler e escrever diferentes formatos de imagem e vídeo (como JPEG, PNG, MP4, etc.), instale as seguintes bibliotecas: 
        ```bash
        sudo apt install -y libjpeg-dev libpng-dev libtiff-dev
        sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
        sudo apt install -y libxvidcore-dev libx264-dev
        sudo apt install -y libfontconfig1-dev libcairo2-dev
        sudo apt install -y libgdk-pixbuf2.0-dev libpango1.0-dev
        sudo apt install -y libgtk2.0-dev libgtk-3-dev
        ```
    3. Instale a biblioteca ATLAS (Automatically Tuned Linear Algebra Software) pois ela ajuda a otimizar operações matemáticas:
        ```bash
        sudo apt install -y libatlas-base-dev
        ```
    4. Instale a biblioteca HDF5 pois ela é útil para armazenar grandes quantidades de dados numéricos.
        ```bash
        sudo apt install -y libhdf5-dev libhdf5-103
        ```
- **Passo 4**: Verificar a instalação    
    - Após a conclusão da instalação, é fundamental verificar se o OpenCV foi instalado corretamente e está acessível pelo Python.
    1. Abra o terminal e inicie o interpretador Python 3:
        ```bash
        python3
        ```
    2. No prompt do Python, tente importar o módulo `cv2` e verifique a versão instalada:
        ```python
        import cv2
        print(cv2.__version__)
        ```
    3. Se o OpenCV estiver instalado corretamente, você verá a versão do OpenCV impressa no terminal, algo como `4.5.3` ou similar.
    4. Saia do interpretador Python digitando:
        ```python
        exit()
        ```
- **Passo 5**: Restaurar o tamanho do Swap
    - Manter um arquivo de swap grande pode diminuir a vida útil do seu cartão microSD. Após a instalação, é uma boa prática restaurá-lo ao tamanho original.    
    1. Edite o arquivo de configuração novamente:
        ```bash
        sudo nano /etc/dphys-swapfile
        ```
    2. Altere o valor de `CONF_SWAPSIZE` de volta para `100`:
        ```bash
        CONF_SWAPSIZE=100
        ```
    3. Salve e saia: Pressione `Ctrl+X`, depois `Y` e `Enter`.
    4. Reinicie o serviço de swap para aplicar as alterações:
        ```bash
        sudo /etc/init.d/dphys-swapfile restart
        ```    

---
### **JupyterLab e Jupyter Notebook (RECOMENDADO)**
- O *Jupyter Notebook* é uma aplicação web que permite criar e compartilhar documentos que contêm código executável, equações, visualizações e texto narrativo. Ele é amplamente utilizado em ciência de dados, aprendizado de máquina, análise estatística e outras áreas que envolvem programação interativa.
- O *JupyterLab* é a interface de próxima geração para o Jupyter Notebook, oferecendo uma experiência mais flexível e poderosa. Ele permite que você trabalhe com múltiplos documentos e painéis em uma única interface, facilitando a organização do seu trabalho.

Este guia irá orientá-lo no processo de transformar seu Raspberry Pi 3 em um servidor de desenvolvimento para ciência de dados e Python, acessível de qualquer computador na sua rede.

#### **1\. Entendendo os Recursos: JupyterLab vs. Notebook Clássico**

Antes de instalar, é importante entender a diferença de consumo de recursos no hardware limitado do Raspberry Pi 3 (1 GB de RAM).

* **Jupyter Notebook (Clássico):**  
  * **Descrição:** A interface original, mais simples e focada em um documento por vez.  
  * **Recursos:** É **significativamente mais leve**. Consome menos RAM e CPU, resultando em uma experiência mais fluida e responsiva no RPi 3\.  
  * **Recomendação:** **Ideal para o Raspberry Pi 3**, pois deixa mais memória livre para o seu código (Pandas, NumPy, etc.), evitando lentidão.  
* **JupyterLab:**  
  * **Descrição:** A interface moderna, que funciona como um mini-ambiente de desenvolvimento (IDE) no navegador, com abas, painéis e terminal integrado.  
  * **Recursos:** É **mais pesado**. Utiliza mais RAM e CPU devido à sua arquitetura complexa. A inicialização é mais lenta e a interface pode parecer menos fluida.  
  * **Recomendação:** Use com cautela no RPi 3, ciente de que o desempenho pode ser impactado.

| Característica | JupyterLab | Jupyter Notebook (Clássico) |
| :---- | :---- | :---- |
| **Uso de RAM (Base)** | Médio a Alto | **Baixo** |
| **Uso de CPU (Interface)** | Médio | **Baixo** |
| **Funcionalidades** | **Muito Altas (IDE)** | Básicas (Editor de Notebook) |
| **Recomendação para RPi 3** | Cautelosa | **Fortemente Recomendado** |

A estratégia a seguir instalará **ambos**, permitindo que você escolha o mais adequado para cada tarefa.

#### **2\. Roteiro de Instalação (Passo a Passo)**

* **Pré-requisitos**
    * Raspberry Pi 3 conectado à sua rede.  
    * Acesso ao terminal do RPi (via SSH ou direto com monitor/teclado).

* **Passo 1: Instalar o Jupyter (Ambas as Interfaces)**

    - Antes de iniciar a instalação, certifique-se de que o `pip` está atualizado:
        ```bash
        python -m pip install --upgrade pip
        ```
    - Instale o Jupyter Notebook e Jupyter Lab:
        ```bash
        pip install jupyter jupyterlab notebook
        ```
    - Reinicie o RPi para garantir que todas as dependências sejam carregadas corretamente:
        ```bash
        sudo reboot
        ```

* **Passo 2: Encontrar o Endereço IP do Raspberry Pi**
    - Para descobrir o ip do RPi, digite no terminal dele:  
        ```bash
        hostname -I
        ```
        Anote o endereço que aparecer (ex: 192.168.1.42).

#### **3\. Utilização Básica (Acesso Remoto)**
Agora que tudo está instalado, você pode iniciar o servidor. Escolha uma das duas opções abaixo.

* **Opção A: Iniciando o Jupyter Notebook (Clássico e Leve)**
    1. No terminal do RPi, execute:  
        ```bash
        jupyter notebook --ip=0.0.0.0 \--no-browser
        ```
        Onde: 
    * `--ip=0.0.0.0`: Permite conexões de qualquer dispositivo na rede.  
    * `--no-browser`: Impede que ele tente abrir um navegador no próprio RPi.  
    2. O terminal exibirá uma saída com um link. Copie a URL que contém o token:
        ```bash  
        http://127.0.0.1:8888/?token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  
        ```
    3. No navegador do seu computador desktop, cole a URL, mas substitua 127.0.0.1 pelo IP do seu Raspberry Pi:  
        ```bash
        http://192.168.1.42:8888/?token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ```
* **Opção B: Iniciando o JupyterLab (Moderno e Completo)**

    1. O processo é idêntico, mudando apenas o comando. No terminal do RPi, execute:  
        ```bash
        jupyter lab --ip=0.0.0.0 --no-browser
        ```
    2. Copie a URL com o token da saída do terminal.  
    3. No navegador do seu computador desktop, cole a URL, substituindo a parte inicial pelo IP do seu Raspberry Pi:  
        ```
        http://192.168.1.42:8888/lab?token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        ```

#### **4\. Dica: Configurando uma Senha Fixa (RECOMENDADO)**
Para não precisar copiar e colar o token toda vez, configure uma senha permanente.
1. Pare o servidor Jupyter se ele estiver rodando (`Ctrl + C` no terminal).  
2. Execute o seguinte comando para gerar os arquivos de configuração:  
    ```bash  
    jupyter server --generate-config
    ```
3. Agora, crie sua senha. O comando pedirá que você digite e confirme a senha desejada:  
    ```bash
    jupyter server password
    ```
- Pronto! Da próxima vez que você iniciar o jupyter notebook ou jupyter lab, basta acessar `http://<IP_DO_SEU_PI>:8888` e a interface pedirá a senha que você acabou de criar.

#### **5\. Dica: Melhore o desempenho do RPi (RECOMENDADO)**
- Execute o Raspberry Pi em Modo Totalmente `Headless` (sem *Graphical User Interphace*-GUI).
- Esta é, de longe, a melhoria mais significativa que você pode fazer. Se você só usa o RPi via SSH, a interface gráfica (GUI) pode estar desperdiçando centenas de megabytes de RAM.  
- **Como fazer:**
    
    1. Abra o terminal (via SSH) e digite:
    
        ```bash
        sudo raspi-config  
        ```
    2. Vá para `System Options -> Boot / Auto Login`.  
    
    3. Selecione a opção `Console (Autologin)`. Isso fará com que o RPi inicie diretamente na linha de comando, sem carregar o ambiente de desktop.  
- **Resultado:** Isso libera cerca de 200-400 MB de RAM que agora estarão disponíveis, tornando a análise de código e a resposta do editor muito mais rápidas.
---
### VSCode (opcional)
O Visual Studio Code (VSCode) é um editor de código-fonte leve, mas poderoso, desenvolvido pela Microsoft. Ele é amplamente utilizado por desenvolvedores devido à sua versatilidade, suporte a várias linguagens de programação e uma vasta gama de extensões que aumentam sua funcionalidade. Para utilizar o VSCode remotamente no Raspberry Pi, siga os passos abaixo:
#### Passo 1: Instalar o VSCode no computador pessoal
1. Acesse o site oficial do [Visual Studio Code](https://code.visualstudio.com/).
2. Baixe a versão apropriada para o seu sistema operacional (Windows, macOS ou Linux).
3. Siga as instruções de instalação fornecidas no site.
#### Passo 2: Instalar a extensão "Remote - SSH"
1. Abra o VSCode no seu computador pessoal.
2. Vá para a aba de extensões clicando no ícone de quadrado no lado esquerdo ou pressionando `Ctrl+Shift+X`.
3. Na barra de pesquisa, digite "Remote - SSH".
4. Clique em "Install" para instalar a extensão.
#### Passo 3: Configurar a conexão SSH
1. Pressione `F1` ou `Ctrl+Shift+P` para abrir a paleta de comandos.
2. Digite "Remote-SSH: Connect to Host..." e selecione essa opção.
3. Clique em "Add New SSH Host...".
4. Insira o comando SSH para se conectar ao seu Raspberry Pi, por exemplo:
    ```bash
    ssh pi@rpi1.local
    ```
5. Escolha o arquivo de configuração SSH (geralmente `~/.ssh/config`).
6. Após adicionar o host, selecione-o na lista para se conectar.
7. A primeira vez que você se conectar, pode ser solicitado que você aceite a chave do host. Digite "yes" e pressione `Enter`.
8. Insira a senha do usuário do Raspberry Pi quando solicitado.
#### Passo 4: Abrir uma pasta no Raspberry Pi
1. Após a conexão, você verá uma nova janela do VSCode.
2. Vá para `File > Open Folder...` e navegue até o diretório no Raspberry Pi onde você deseja trabalhar.
3. Clique em "OK" para abrir a pasta.
#### Passo 5: **Para liberar mais recursos no RPi ao utilizar o VSCode** (RECOMENDADO)
O VSCode é uma aplicação relativamente pesada, e o Raspberry Pi 3B tem recursos limitados. Aqui estão algumas dicas para melhorar o desempenho ao usar o VSCode remotamente:
1. Otimize as Configurações do Workspace no VS Code:  
O VS Code Server "monitora" a todas as pastas e arquivos do seu projeto para detectar mudanças, o que consome muita CPU. Você pode instruí-lo a ignorar diretórios que não precisam ser monitorados.  
   * **Como fazer:** Dentro do seu projeto no VS Code, crie uma pasta .vscode e dentro dela um arquivo settings.json. Adicione o seguinte conteúdo:

   ```json  
    {
    "files.watcherExclude": {
        "**/.git/objects/**": true,
        "**/.git/subtree-cache/**": true,
        "**/node_modules/*/**": true,
        "**/.venv/**": true,
        "**/__pycache__/**": true,
        "**/build/**": true,
        "**/dist/**": true
    },
    "search.exclude": {
        "**/node_modules": true,
        "**/bower_components": true,
        "**/*.code-search": true,
        "**/.venv": true,
        "**/build": true,
        "**/dist": true
    }
    }
    ```
   * **O que isso faz?** Impede que o VS Code gaste recursos monitorando e indexando pastas de dependências (`node_modules`, `.venv`), cache (`__pycache__`) ou de compilação (`build`, `dist`). A diferença na responsividade é considerável, especialmente ao abrir grandes projetos.  
2. Desative Extensões Pesadas ou Desnecessárias (no Remote):  
   Lembre-se: as extensões rodam no RPi, não no seu computador pessoal. Extensões de temas e de interface rodam localmente, mas as de linguagem (Python, C++, Docker) rodam remotamente.  
   * **Como fazer:**  
     1. Com a sessão remota conectada, vá para a aba de Extensões.  
     2. Você verá seções `Local` e `SSH: o_seu_rpi`  
     3. Desabilite no ambiente remoto (`Disable (Workspace)`) qualquer extensão que não seja absolutamente essencial para o projeto atual. O `Pylance`, por exemplo, é poderoso mas consome muita memória. Para edições rápidas, você pode desabilitá-lo temporariamente.
