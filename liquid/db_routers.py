class ModelDatabaseRouter(object):
    """
    Allows a model to choose which DB it uses
    Currently used by the Caffeine frontend
    Specify the DB a model should use by setting in_db in the model's Meta class
    """

    def db_for_read(self, model, **hints):
        if hasattr(model._meta, 'in_db'):
            return model._meta.in_db
        return None

    def db_for_write(self, model, **hints):
        if hasattr(model._meta, 'in_db'):
            return model._meta.in_db        
        return None

    def allow_syncdb(self, db, model):
        if hasattr(model._meta, 'in_db'):
            return model._meta.in_db == db
        else:
            # Models that don't specify a DB can only go to 'default'
            return db == 'default'
