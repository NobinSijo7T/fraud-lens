"""
Train the phishing detection model on the phishing dataset.
This script trains the phishing URL classifier and saves the model artifacts.
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.app.services import training_service

def main():
    print("🔗 Training Phishing Detection Model")
    print("=" * 60)
    
    dataset_id = "phishing_links_url/Dataset.csv"
    
    try:
        print(f"📊 Loading dataset: {dataset_id}")
        print("⚙️  Training models (Logistic Regression, Decision Tree, Random Forest)...")
        
        result = training_service.train(dataset_id=dataset_id, task='phishing')
        
        print("\n✅ Training completed successfully!")
        print(f"📦 Selected model: {result['selected_model']}")
        print(f"🎯 Target column: {result['target_column']}")
        print(f"📈 Features used: {len(result['features'])} features")
        print(f"⏰ Trained at: {result['trained_at']}")
        
        # Display evaluation metrics
        evaluation = training_service.evaluation('phishing')
        if evaluation:
            print("\n📊 Model Performance:")
            selected = evaluation['selected_model']
            metrics = evaluation['models'][selected]
            print(f"   Accuracy: {metrics['accuracy']:.2%}")
            print(f"   Precision: {metrics['precision']:.2%}")
            print(f"   Recall: {metrics['recall']:.2%}")
            print(f"   F1 Score: {metrics['f1_score']:.2%}")
            if metrics['roc_auc']:
                print(f"   ROC AUC: {metrics['roc_auc']:.2%}")
        
        print("\n🎉 Phishing model is now ready for predictions!")
        print("   You can test it from the Analyze page in the frontend.")
        
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
