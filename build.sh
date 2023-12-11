#!/bin/bash

mkdir -p pkg
cp manifest.json pkg
cp logo.png pkg/icon.png
cp README.md pkg
cp PostChat/bin/Debug/netstandard2.1/PostChat.dll pkg
cd pkg
zip -vr ../PostChat.zip *