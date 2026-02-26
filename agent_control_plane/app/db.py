from sqlmodel import Session, SQLModel, create_engine

engine = create_engine("sqlite:///./agent_control_plane.db", echo=False)


def create_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
