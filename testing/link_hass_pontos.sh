#!/bin/bash

# Define paths
SOURCE_DIR=~/hass-pontos/custom_components/hass_pontos
TARGET_DIR=~/.homeassistant/custom_components

# Navigate to the parent directory of the target folder
cd $TARGET_DIR

# Remove the existing directory and create a new one
sudo rm -rf hass_pontos
mkdir hass_pontos

# Create hard links for the main files
sudo ln $SOURCE_DIR/* $TARGET_DIR/hass_pontos/

# Navigate to the hass_pontos directory
cd hass_pontos

# Create the translations directory and hard link the translation files
mkdir translations
cd translations
sudo ln $SOURCE_DIR/translations/* .

echo "Hard linking completed successfully!"
