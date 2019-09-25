# clear any previous runs
rm -fr bin *_pb.js include protoc protoc*.zip readme.txt

wget https://github.com/protocolbuffers/protobuf/releases/download/v3.9.2/protoc-3.9.2-linux-x86_64.zip

unzip protoc*.zip
mv bin/protoc protoc
rm -fr bin *_pb.js include protoc*.zip readme.txt
