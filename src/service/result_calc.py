


from database.repo.partipicant import ParticipantRepository
from database.repo.result_participant import ResultParticipantRepository
from database.repo.try_festival import TryFestivalRepository


class RelsultCalcService:
    
    def __init__(
        self,
        result_participant_repo: ResultParticipantRepository,
        try_festival_repo: TryFestivalRepository,
    ) -> None:
        self._result_participant_repo = result_participant_repo
        self._try_festival_repo = try_festival_repo
        
    async def festival_result_calc():
        pass