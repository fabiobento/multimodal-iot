#!/bin/bash

# Script para instalar o OpenCV no Raspberry Pi.

echo "----------------------------------------------------"
echo "Passo 1: Preparando o Raspberry Pi..."
echo "----------------------------------------------------"
echo "Atualizando a lista de pacotes e o sistema. Isso pode levar alguns minutos."
sudo apt update -y

echo "----------------------------------------------------"
echo "Passo 2: Aumentando o espaço de Swap para 2GB..."
echo "----------------------------------------------------"
# Altera a configuração de SWAPSIZE para 2048
sudo sed -i 's/CONF_SWAPSIZE=[0-9]*/CONF_SWAPSIZE=2048/' /etc/dphys-swapfile
echo "Arquivo /etc/dphys-swapfile atualizado."
sudo /etc/init.d/dphys-swapfile restart
echo "Serviço de swap reiniciado com 2GB."

echo "----------------------------------------------------"
echo "Passo 3: Instalando o OpenCV e suas dependências..."
echo "----------------------------------------------------"
# Instala a biblioteca principal do OpenCV para Python 3
sudo apt install python3-opencv -y

# Instala bibliotecas para formatos de imagem e vídeo
sudo apt install -y libjpeg-dev libpng-dev libtiff-dev
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt install -y libxvidcore-dev libx264-dev
sudo apt install -y libfontconfig1-dev libcairo2-dev
sudo apt install -y libgdk-pixbuf2.0-dev libpango1.0-dev
sudo apt install -y libgtk2.0-dev libgtk-3-dev

# Instala a biblioteca de otimização matemática ATLAS
sudo apt install -y libatlas-base-dev

# Instala a biblioteca HDF5 para manipulação de grandes volumes de dados
sudo apt install -y libhdf5-dev libhdf5-103

echo "Dependências do OpenCV instaladas."

echo "----------------------------------------------------"
echo "Passo 4: Verificando a instalação do OpenCV..."
echo "----------------------------------------------------"
# Executa um comando Python para importar o cv2 e imprimir a versão
OPENCV_VERSION=$(python3 -c "import cv2; print(cv2.__version__)")

if [ $? -eq 0 ]; then
  echo "OpenCV instalado com sucesso! Versão: $OPENCV_VERSION"
else
  echo "ERRO: A instalação do OpenCV falhou. Não foi possível importar o módulo 'cv2' no Python."
  exit 1
fi

echo "----------------------------------------------------"
echo "Passo 5: Restaurando o tamanho do Swap para 100MB..."
echo "----------------------------------------------------"
# Restaura a configuração de SWAPSIZE para 100
sudo sed -i 's/CONF_SWAPSIZE=[0-9]*/CONF_SWAPSIZE=100/' /etc/dphys-swapfile
echo "Arquivo /etc/dphys-swapfile restaurado."
sudo /etc/init.d/dphys-swapfile restart
echo "Serviço de swap reiniciado com 100MB."

echo "----------------------------------------------------"
echo "Instalação do OpenCV concluída!"
echo "É recomendado reiniciar o sistema para garantir que todas as alterações sejam aplicadas."
echo "Execute: sudo reboot"
echo "----------------------------------------------------"