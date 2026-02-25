# **Instalação do Edge Impulse Linux CLI e SDK no Raspberry Pi**

Este tutorial guiará você pelo processo de instalação e configuração do **Edge Impulse Linux CLI** no Raspberry Pi conforme descrito pela documentação em [Edge Impulse CLI Installation](https://docs.edgeimpulse.com/tools/clis/edge-impulse-cli/installation#linux%2C-ubuntu%2C-macos%2C-and-raspbian-os) e no [Edge Impulse SDk Instalation->Raspberry Pi](https://docs.edgeimpulse.com/hardware/boards/raspberry-pi-4).

## **Passo 1: Configurações Iniciais do Raspberry Pi**

Antes de executar esse tutorial você deve ter realizado o tutorial  [Configurações iniciais do Raspberry Pi(RPi)](../rpi_basic_config/rpi_basic_config.md). Antes de começarmos, certifique-se de que o Raspberry Pi está atualizado e com as configurações básicas prontas. Se necessário, revise as etapas iniciais de configuração do Raspberry Pi, como a habilitação da interface de câmera e a conexão com a rede. 

## **Passo 2: Executar o Script para Instalação das Ferramentas CLI**

* No terminal do seu computador pessoal digite, substituindo **\<hostname\>** pelo nome de acordo com sua bancada (para a bancada 1, por exemplo, seria `ssh pi@rpi1.local`) 

```bash
ssh pi@<hostname>.local
```

* Em seguida forneça a senha `pi` cadastrada no `rpi-mager`:

```bash
pi@<hostname>.local's password:
```

* Em seguida você verá o prompt do terminal parecido com a figura abaixo, indicando que você está conectado com o usuário “pi” no host “rpi1”(o número final depende de seu hostname) :

```bash
pi@rpi1:\~ $
```
* Agora que vocês está conectado ao RPi por SSH, digite os seguintes comandos para instalar as ferramentas do Edge Impulse CLI:
  1. Faça o download do seguinte script para instalação das ferramentas do Edge Impulse:
    ```bash
     wget https://raw.githubusercontent.com/fabiobento/sis-emb-2025-2/refs/heads/main/aulas/sbc-rpi/rpi_ei_linux/scripts/install_ei_linux_cli_tools.sh
    ```    
  2. No mesmo diretório em que baixou o script acima, conceda permissão de execução:
    ```bash
    chmod +x install_ei_linux_cli_tools.sh
    ```
  3. Agora execute o script:
    ```bash
    ./install_ei_linux_cli_tools.sh
    ```

  O script acima realizará as seguintes etapas:
    * Atualização do sistema operacional do Raspberry Pi
    * Instalação do Node.js e suas dependências
    * Instalação do Edge Impulse CLI (Central de desenvolvimento)
    * Instalação do Edge Impulse para Linux (Executor de Inferência)

  ### O que é o Node.js? 
    O Node.js é um ambiente de execução de código JavaScript do lado do servidor, construído sobre o motor V8 do Google Chrome. Ele permite que os desenvolvedores executem código JavaScript fora do navegador, possibilitando a criação de aplicações de servidor escaláveis e de alta performance. O Node.js é amplamente utilizado para desenvolver aplicações web, APIs, ferramentas de linha de comando e muito mais, graças à sua capacidade de lidar com operações assíncronas e eventos em tempo real. Segue a [documentação oficial do Node.js](https://nodejs.org/en/about/) para mais informações.
  ### O que é o Edge Impulse CLI (Central de desenvolvimento)? 
    O edge-impulse-cli é uma suíte de ferramentas de propósito geral que serve como a principal ponte entre o seu ambiente de desenvolvimento local e os projetos na nuvem do Edge Impulse Studio. Suas principais funcionalidades incluem:
    * **Coleta de Dados:** Através de ferramentas como o edge-impulse-data-forwarder, é possível conectar uma vários tipos de microcontroladores e sensores ao seu computador e enviar os dados diretamente para o seu projeto no Edge Impulse.  
    * **Gerenciamento de Dispositivos:** Permite o controle de dispositivos locais conectados, atuando como um proxy para sincronizar dados de placas que não possuem conexão direta com a internet.  
    * **Upload de Arquivos:** Facilita o envio de conjuntos de dados já existentes (como arquivos de áudio, imagens ou CSV) para a plataforma.  
    * **Execução de Impulsos em Dispositivos Conectados:** Com o comando edge-impulse-run-impulse, é possível testar o seu modelo (impulso) em tempo real no dispositivo que está coletando os dados.  
    * **Flash de Firmware:** Inclui utilitários para gravar o firmware em placas de desenvolvimento específicas.

    Em resumo, o edge-impulse-cli é uma ferramenta usada durante a fase de coleta de dados, treinamento e iteração do seu modelo de Machine Learning. Seguem um link para a [documentação oficial do Edge Impulse CLI](https://docs.edgeimpulse.com/tools/clis/edge-impulse-cli) para mais informações.
  ### O que é o Edge Impulse para Linux (Executor de Inferência)
    O edge-impulse-linux é uma ferramenta especializada, focada na etapa de implantação do seu modelo treinado em dispositivos que rodam um sistema operacional Linux, como Raspberry Pi, NVIDIA Jetson Nano ou qualquer computador com arquitetura x86_64, ARMv7 ou AARCH64. Suas características centrais são:
      * **Download de Modelos Compilados:** A principal função, executada através do edge-impulse-linux-runner, é baixar o seu impulso treinado como um arquivo executável autocontido (.eim).  
      * **Execução de Inferência Local:** Permite que você execute o modelo (.eim) diretamente no dispositivo Linux para realizar a inferência, ou seja, fazer previsões com base em novos dados.  
      * **Otimização para a Arquitetura Alvo:** Os modelos `.eim` são compilados e otimizados especificamente para a arquitetura do processador do seu dispositivo Linux, garantindo o melhor desempenho possível.  
      * **SDKs para Integração:** Fornece Kits de Desenvolvimento de Software (SDKs) para linguagens como Python, Node.js e Go, permitindo que você integre facilmente a execução do modelo em suas próprias aplicações.

    Essencialmente, o `edge-impulse-linux` é usado quando o seu modelo está treinado e pronto para ser implantado em um dispositivo Linux para uso em um produto ou aplicação final. Segue um link para a [documentação oficial do Edge Impulse para Linux](https://docs.edgeimpulse.com/tools/clis/edge-impulse-linux) para mais informações.