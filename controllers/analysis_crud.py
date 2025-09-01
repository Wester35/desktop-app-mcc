from sqlalchemy.orm import Session
from sqlalchemy import desc
from models.data_models import AnalysisResult
from datetime import datetime


def save_analysis_result(db: Session, year: int, integrated_index: float):
    """Сохранение результата анализа"""
    try:
        # Удаляем старый результат если есть
        old_result = db.query(AnalysisResult).filter(AnalysisResult.year == year).first()
        if old_result:
            db.delete(old_result)

        result = AnalysisResult(
            year=year,
            integrated_index=integrated_index,
            created_at=datetime.now()
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        return result
    except Exception as e:
        db.rollback()
        raise e


def get_analysis_results(db: Session):
    """Получение всех результатов анализа"""
    return db.query(AnalysisResult).order_by(AnalysisResult.year).all()


def get_last_analysis(db: Session):
    """Получение последнего анализа"""
    return db.query(AnalysisResult).order_by(desc(AnalysisResult.created_at)).first()