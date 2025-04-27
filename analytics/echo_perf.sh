# prints out results for all datasets 

# Get lambda_d value from command line argument
if [ -z "$1" ]; then
    echo "Error: lambda_d parameter is required"
    echo "Usage: $0 <lambda_d> <model_type> <dataset_name>"
    echo "Example: $0 0.0001 vk kaengreg/rus-scifact"
    echo "         $0 0.0001 ai-forever kaengreg/rus-scifact"
    exit 1
fi

LAMBDA_D=$1

if [ -z "$2" ]; then
    echo "Error: model type parameter is required" 
    echo "Usage: $0 <lambda_d> <model_type> <dataset_name>"
    echo "Example: $0 0.0001 vk kaengreg/rus-scifact"
    echo "         $0 0.0001 ai-forever kaengreg/rus-scifact"
    exit 1
fi

if [ "$2" != "vk" ] && [ "$2" != "ai-forever" ]; then
    echo "Error: model_type must be either 'vk' or 'ai-forever'"
    exit 1
fi

MODEL_TYPE=$2

RES_DIR=splade-doc-results/${MODEL_TYPE}_rusbeir_${LAMBDA_D}


DATASETS=("kaengreg/rus-scifact" "kaengreg/rubq" "kaengreg/rus-arguana" "kaengreg/rus-nfcorpus" "kaengreg/rus-tydiqa" "kaengreg/rus-xquad")

for DATASET in "${DATASETS[@]}"; do
    echo "Printing results for dataset: $DATASET"
    echo "Results directory: $RES_DIR/$DATASET/perf.json"
    cat $RES_DIR/$DATASET/perf.json
    echo "----------------------------------------"
done





