# данный скрипт позволяет быстро создать архив модели / распаковать модель

# пример использования:
# bash zip_ru-splade-doc.sh 0.0001 vk zip 
# bash zip_ru-splade-doc.sh 0.0001 ai-forever zip
# bash zip_ru-splade-doc.sh 0.0001 vk unzip
# bash zip_ru-splade-doc.sh 0.0001 ai-forever unzip



# уточняем у пользователя параметры модели, чтобы определить путь к этой модели!

if [ -z "$1" ]; then
    echo "Error: lambda_d parameter is required"
    echo "Usage: $0 <lambda_d>"
    echo "Example: $0 0.0001" 
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
MODEL_DIR=models/${MODEL_TYPE}_ru-splade-doc_${LAMBDA_D}



if [ "$3" != "unzip" ] && [ "$3" != "zip" ]; then
    echo "Error: mode must be either 'unzip' or 'zip'"
    exit 1
fi


ACTION=$3


if [ "$ACTION" = "zip" ]; then
    # Create gzip archive of model directory
    tar -czf ${MODEL_DIR}.tar.gz ${MODEL_DIR}
fi

if [ "$ACTION" = "unzip" ]; then
    # Unzip model archive if needed
    tar -xzf ${MODEL_DIR}.tar.gz
fi





