export PYTHONPATH=$PYTHONPATH:$(pwd)
export SPLADE_CONFIG_NAME="ru-splade-doc.yaml" 
  
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

if [ "$MODEL_TYPE" = "vk" ]; then
    MODEL_NAME="deepvk/RuModernBERT-base"
else
    MODEL_NAME="ai-forever/ruBert-base"
fi

CHECKPOINT_DIR=models/${MODEL_TYPE}_ru-splade-doc_${LAMBDA_D}/checkpoint
INDEX_DIR=models/${MODEL_TYPE}_ru-splade-doc_${LAMBDA_D}/index
OUT_DIR=models/${MODEL_TYPE}_ru-splade-doc_${LAMBDA_D}/out



DATASETS=("kaengreg/rus-scifact" "kaengreg/rubq" "kaengreg/rus-arguana" "kaengreg/rus-nfcorpus" "kaengreg/rus-tydiqa" "kaengreg/rus-xquad")

for DATASET_NAME in "${DATASETS[@]}"; do
    echo "Processing dataset: $DATASET_NAME"
    
    DATASET_DIR=${OUT_DIR}/rusbeir/${DATASET_NAME}
    
    echo "Dataset will be saved in: $DATASET_DIR"
    
    if [ -d "$DATASET_DIR" ]; then
        echo "Dataset $DATASET_NAME already exists! Skipping..."
        continue
    fi

    python -m splade.rusbeir_eval \
        +config.checkpoint_dir=$CHECKPOINT_DIR \
        +config.index_dir=$INDEX_DIR \
        +config.out_dir=$OUT_DIR \
        config.regularizer.FLOPS.lambda_q=0.0000 \
        config.regularizer.FLOPS.lambda_d=$LAMBDA_D \
        +config.random_seed=60 \
        init_dict.model_type_or_dir=$MODEL_NAME \
        config.tokenizer_type=$MODEL_NAME \
        +rusbeir.dataset=$DATASET_NAME

    echo "Finished processing $DATASET_NAME"
    echo "----------------------------------------"
done

exit 0