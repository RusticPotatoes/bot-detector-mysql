# script to insert all the data we need
import random
from datetime import datetime, timedelta

from sqlalchemy import (
    create_engine,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import (
    Players,
    Skills,
    Activities,
    PlayerActivities,
    PlayerSkills,
    Report,
    ScraperData,
    Labels,
)

Base = declarative_base()
random.seed(42)

# Define other SQLAlchemy models for remaining tables in a similar manner

# Create an engine and bind the base
engine = create_engine("mysql+pymysql://root:root_bot_buster@mysql:3306/playerdata")
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


# Define function to generate random date within a year
def random_date():
    return datetime.utcnow() - timedelta(days=random.randint(0, 365))


def get_labels():
    # Query the labels table to get all id values
    label_ids = session.query(Labels.id).all()
    label_ids = [id[0] for id in label_ids]  # Convert list of tuples to list of ids
    return label_ids


def insert_players(len_players, label_ids: list):
    # Insert data into Players table
    for i in range(len_players):
        print(f"Player_{i}")
        # Check if the player already exists
        existing_player = session.query(Players).filter_by(name=f"Player_{i}").first()
        if not existing_player:
            player = Players(
                name=f"Player_{i}",
                created_at=random_date(),
                updated_at=random_date(),
                possible_ban=random.choice([True, False]),
                confirmed_ban=random.choice([True, False]),
                confirmed_player=random.choice([True, False]),
                label_id=random.choice(label_ids),  # Select a random id from label_ids
                label_jagex=random.randint(0, 2),
                normalized_name=f"Player_{i}",
            )
            session.add(player)
    session.commit()
    return


def get_skills():
    # Query the skills table to get all id values
    skill_ids = session.query(Skills.skill_id).all()
    skill_ids = [id[0] for id in skill_ids]  # Convert list of tuples to list of ids
    return skill_ids


def get_activities():
    # Query the activity table to get all id values
    activity_ids = session.query(Activities.activity_id).all()
    activity_ids = [
        id[0] for id in activity_ids
    ]  # Convert list of tuples to list of ids
    return activity_ids


def insert_scraper_data(len_scraper_data, len_players, skill_ids, activity_ids):
    for i in range(1, len_scraper_data + 1):
        print(f"scraper_data_{i}")
        # pick random player
        player_id = random.randint(1, len_players)

        # pick random amount of skills
        amount_skills = random.randint(0, len(skill_ids))
        random.shuffle(skill_ids)
        skills = skill_ids[:amount_skills]

        # pick random amount of activities
        amount_activities = random.randint(0, len(activity_ids))
        random.shuffle(activity_ids)
        activities = activity_ids[:amount_activities]

        # scraper data
        try:
            session.add(
                ScraperData(scraper_id=i, player_id=player_id, created_at=random_date())
            )
            session.commit()
            for skill in skills:
                session.add(
                    PlayerSkills(
                        scraper_id=i,
                        skill_id=skill,
                        skill_value=random.randint(1, 200_000_000),
                    )
                )
            for activity in activities:
                session.add(
                    PlayerActivities(
                        scraper_id=i,
                        activity_id=activity,
                        activity_value=random.randint(1, 65_000),
                    )
                )
        except IntegrityError:
            session.rollback()  # Rollback the transaction if a duplicate entry is encountered
        finally:
            session.commit()


def insert_reports(len_reports, len_players):
    for i in range(1, len_reports + 1):
        print(f"Report_{i}")
        # pick random player
        reporter = random.randint(1, len_players)
        reported = random.randint(1, len_players)

        if reporter == reported:
            reported = random.randint(1, len_players)

        try:
            session.add(
                Report(
                    created_at=random_date(),
                    reportedID=reporter,
                    reportingID=reported,
                    region_id=random.randint(1, 30000),
                    x_coord=random.randint(1, 30000),
                    y_coord=random.randint(1, 30000),
                    z_coord=random.randint(1, 30000),
                    timestamp=random_date(),
                    manual_detect=random.choice([0, 1]),
                    on_members_world=random.choice([0, 1]),
                    on_pvp_world=random.choice([0, 1]),
                    world_number=random.randint(1, 300),
                    equip_head_id=random.randint(1, 30000),
                    equip_amulet_id=random.randint(1, 30000),
                    equip_torso_id=random.randint(1, 30000),
                    equip_legs_id=random.randint(1, 30000),
                    equip_boots_id=random.randint(1, 30000),
                    equip_cape_id=random.randint(1, 30000),
                    equip_hands_id=random.randint(1, 30000),
                    equip_weapon_id=random.randint(1, 30000),
                    equip_shield_id=random.randint(1, 30000),
                    equip_ge_value=random.randint(1, 2000000000),
                )
            )
        except IntegrityError:
            session.rollback()  # Rollback the transaction if a duplicate entry is encountered
        finally:
            session.commit()


def main():
    len_players = 250
    label_ids = get_labels()
    insert_players(len_players, label_ids)
    skill_ids = get_skills()
    activity_ids = get_activities()
    len_scraper_data = len_players * 3
    insert_scraper_data(len_scraper_data, len_players, skill_ids, activity_ids)
    insert_reports(len_reports=10000, len_players=len_players)


if __name__ == "__main__":
    main()
