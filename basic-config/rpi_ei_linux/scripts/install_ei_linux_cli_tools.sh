#!/bin/bash

# Script para automatizar a instalação do Edge Impulse Linux CLI e SDK
# com base no documento rpi_ei_linux.md

echo "----------------------------------------------------"
echo "Passo 2: Atualizando o Sistema..."
echo "----------------------------------------------------"
sudo apt update -y
sudo apt upgrade -y

echo "----------------------------------------------------"
echo "Passo 3: Instalando Node.js e dependências..."
echo "----------------------------------------------------"
# Adiciona o repositório do Node.js v22.x
echo "Adicionando repositório do Node.js..."
curl -sL https://deb.nodesource.com/setup_22.x | sudo -E bash -

# Instala o Node.js e outras dependências
echo "Instalando Node.js, GCC, G++, Make, SOX e GStreamer..."
sudo apt install -y gcc g++ make build-essential nodejs sox gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-base gstreamer1.0-plugins-base-apps

# Limpa pacotes que não são mais necessários
echo "Limpando pacotes desnecessários..."
sudo apt autoremove -y

# Verifica a versão do Node.js
echo "Verificando a versão do Node.js..."
node -v

echo "----------------------------------------------------"
echo "Configurando o diretório global do NPM..."
echo "----------------------------------------------------"
# Cria o diretório e configura o prefixo para o npm
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'

# Adiciona o novo diretório ao PATH nos arquivos de perfil para que os comandos fiquem disponíveis
# A verificação 'grep' evita que a linha seja adicionada múltiplas vezes
if ! grep -q "export PATH=~/.npm-global/bin:\$PATH" ~/.profile; then
  echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.profile
  echo "Diretório NPM adicionado ao seu ~/.profile."
fi
if ! grep -q "export PATH=~/.npm-global/bin:\$PATH" ~/.bashrc; then
  echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
  echo "Diretório NPM adicionado ao seu ~/.bashrc."
fi

# Exporta o PATH para a sessão atual, para que os próximos comandos funcionem
export PATH=~/.npm-global/bin:$PATH
echo "PATH atualizado para a sessão atual."

echo "----------------------------------------------------"
echo "Passo 4: Instalando o Edge Impulse CLI..."
echo "AVISO: Este passo pode demorar vários minutos no Raspberry Pi."
echo "----------------------------------------------------"
npm install edge-impulse-cli -g --unsafe-perm

echo "----------------------------------------------------"
echo "Passo 5: Instalando o Edge Impulse para Linux..."
echo "AVISO: Este passo também pode demorar vários minutos."
echo "----------------------------------------------------"
npm install edge-impulse-linux -g --unsafe-perm

echo "----------------------------------------------------"
echo "Passo 6: Corrigindo permissões de execução..."
echo "----------------------------------------------------"
# Garante que os scripts instalados possam ser executados
chmod +x ~/.npm-global/bin/*
echo "Permissões de execução aplicadas aos comandos do Edge Impulse."

echo "----------------------------------------------------"
echo "Instalação concluída com sucesso!"
echo ""
echo "Para garantir que as alterações de PATH sejam permanentes,"
echo "feche e reabra seu terminal ou execute o comando:"
echo "source ~/.bashrc"
echo ""
echo "Depois, você pode verificar a instalação com os comandos:"
echo "edge-impulse-data-forwarder --clean"
echo "edge-impulse-linux --clean"
echo "----------------------------------------------------"