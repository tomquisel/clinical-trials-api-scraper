import logging
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.ext.automap import automap_base


from clinical_trials_api_scraper.clients.trials_store_interface_base import (
    TrialsStoreInterfaceBase,
)
import clinical_trials_api_scraper.utils.trial_model_utils as tmu


DB_SCHEMA = "trials_status_schema"

logger = logging.getLogger(__name__)

Base = automap_base(metadata=MetaData(schema=DB_SCHEMA))


class Organization(Base):
    __tablename__ = "organizations"


class Trial(Base):
    __tablename__ = "trials"


class SqlTrialsStoreClient(TrialsStoreInterfaceBase):
    db_name = "clinical_trials_status"

    def __init__(self):
        self.engine = create_engine(
            "postgres://postgres:1234@db:5432/{}".format(self.db_name), echo=False
        )
        Base.prepare(self.engine, reflect=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        logger.info(Trial.__table__.columns)
        logger.info(Organization.__table__.columns)

    def store_trials_batch(self, trials_batch):
        logger.info("storing {} values".format(len(trials_batch)))
        trials = [tmu.trial_from_response_data(t) for t in trials_batch]
        trials = [tmu.add_computed_fields(t) for t in trials]
        for full_trial in trials:
            organization, trial = tmu.split_organization_trial(full_trial)
            org_obj = Organization(**organization)

            trial["organization"] = org_obj
            trial_obj = Trial(**trial)
            self.session.merge(trial_obj)
            # logger.info(f"storing trial {trial_obj.id} from {inst_obj.org_full_name}")
        self.session.commit()
        logger.info("Batch stored.")

    def is_ready(self):
        return True
