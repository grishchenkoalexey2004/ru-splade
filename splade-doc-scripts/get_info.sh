# prints all metrics of model 



export PYTHONPATH=$PYTHONPATH:$(pwd)
export SPLADE_CONFIG_NAME="ru-splade-doc.yaml" 
  
# Get lambda_d value from command line argument
if [ -z "$1" ]; then
    echo "Error: lambda_d parameter is required"
    echo "Usage: $0 <lambda_d> <model_type>"
    echo "Example: $0 0.0001 vk"
    echo "         $0 0.0001 ai-forever"
    exit 1
fi

LAMBDA_D=$1

if [ -z "$2" ]; then
    echo "Error: model type parameter is required" 
    echo "Usage: $0 <lambda_d> <model_type>"
    echo "Example: $0 0.0001 vk"
    echo "         $0 0.0001 ai-forever"
    exit 1
fi

if [ "$2" != "vk" ] && [ "$2" != "ai-forever" ]; then
    echo "Error: model_type must be either 'vk' or 'ai-forever'"
    exit 1
fi

MODEL_TYPE=$2

INDEX_DIR=models/${MODEL_TYPE}_ru-splade-doc_${LAMBDA_D}/index
OUT_DIR=models/${MODEL_TYPE}_ru-splade-doc_${LAMBDA_D}/out


cd $INDEX_DIR
echo "Index L_0: " 
cat index_stats.json

echo "Index size:"
du array_index.h5py

cd ../out

echo "flops stats:"
cat flops.json

cd shrinked_dataset

echo "Ranking metrics:"
cat perf.json


cd stats
echo "query stats:"
cat q_stats.json













