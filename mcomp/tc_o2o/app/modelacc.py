from sklearn.linear_model import LogisticRegression  # 逻辑回归
from sklearn.neural_network import MLPClassifier  # 多层感知机
from sklearn.neighbors import KNeighborsClassifier  # K最近邻
from sklearn.svm import SVC  # 支持向量机
from sklearn.gaussian_process import GaussianProcessClassifier  # 高斯过程
from sklearn.gaussian_process.kernels import RBF  # 高斯核函数
from sklearn.tree import DecisionTreeClassifier  # 决策树
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier,\
    ExtraTreesClassifier, BaggingClassifier  # 集成方法
from sklearn.naive_bayes import GaussianNB  # 高斯朴素贝叶斯
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis, LinearDiscriminantAnalysis  # 判别分析
from xgboost import XGBClassifier  # 极端梯度提升（eXtreme Gradient Boosting）
from warnings import filterwarnings
filterwarnings('ignore')  # 忽略警告
import datetime
import evaluation

# 建模、设定参数
classifiers = [
    ('Logistic Regression', LogisticRegression()),  # 逻辑回归
    #('Nearest Neighbors', KNeighborsClassifier(3)),  # K最近邻
    #('Linear SVM', SVC(kernel='linear', C=0.025)),  # 线性的支持向量机
    #('RBF SVM', SVC(gamma=2, C=1)),  # 径向基函数的支持向量机
    #('Gaussian Process', GaussianProcessClassifier(1.0 * RBF(1.0))),  # 基于拉普拉斯近似的高斯过程
    ('Decision Tree', DecisionTreeClassifier(max_depth=5)),  # 决策树
    ('Random Forest', RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)),  # 随机森林
    ('AdaBoost', AdaBoostClassifier()),  # 通过迭代弱分类器而产生最终的强分类器的算法
    ('Extra Trees', ExtraTreesClassifier()),
    ('GradientBoosting', GradientBoostingClassifier()),  # 梯度提升树
    ('Bagging', BaggingClassifier()),
    ('Naive Bayes', GaussianNB()),  # 朴素贝叶斯
    #('QDA', QuadraticDiscriminantAnalysis()),  # 二次判别分析
    ('LDA', LinearDiscriminantAnalysis()),  # 线性判别分析
    ('MLP', MLPClassifier(alpha=1)),  # 多层感知机
    ('XGB', XGBClassifier()),  # 极端梯度提升
]

# 输入初始模型，输出得分
def count_fenshu(model,x_train,y_train,x_test,y_test,valid):
    model.fit(x_train, y_train)
    y_pre = model.predict(x_test)
    y_prob = model.predict_proba(x_test)
    cc = evaluation.get_official_auc(y_prob[:,1],y_test,valid)
    return cc

# 
def hodgepodge(classifiers,x_train,y_train,x_test,y_test,valid):
    """大乱炖，用很多函数进行初始评估"""
    model_name = []
    model_score = []
    for name,clf in classifiers:
        #print(name+'star'+"=="*10,datetime.datetime.now(),)
        score = count_fenshu(clf,x_train,y_train,x_test,y_test,valid)
        model_name.append(name)
        model_score.append(score)
        print(name,score,'\t')
    return model_name,model_score

def output_modelscores(model_name,model_score):
    for a,b in zip(model_name,model_score):
        print('{0:22}{1:8}'.format(a,b))

