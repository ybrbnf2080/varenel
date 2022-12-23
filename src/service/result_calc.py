from datetime import timedelta
from typing import Dict, List
from unittest import result

from src.database.repo.partipicant import (
    ParticipantRepository,
)
from src.database.repo.result_participant import (
    ResultParticipantRepository,
)
from src.database.repo.try_festival import (
    TryFestivalRepository,
)
from src.lib import enums
from src.lib.models import (
    Participant,
    ResultParticipant,
    SuperResultParticipant,
    TryFestival,
)


class RelsultCalcService:
    def __init__(
        self,
        participant_repo: ParticipantRepository,
        result_participant_repo: ResultParticipantRepository,
        try_festival_repo: TryFestivalRepository,
    ) -> None:
        self._participant_repo = participant_repo
        self._result_participant_repo = result_participant_repo
        self._try_festival_repo = try_festival_repo

    async def festival_result_calc(self, group: enums.Group) -> List[Dict[str, str]]:
        results = await self._festival_result_calc(group)
        await self._write_result_to_database(results)

        return results

    async def _festival_result_calc(
        self, group: enums.Group
    ) -> List[ResultParticipant]:
        participants: List[
            Participant
        ] = await self._participant_repo.get_all_from_group(group=group)
        final_results: List[ResultParticipant] = []

        for participant in participants:
            results: List[
                TryFestival
            ] = await self._try_festival_repo.get_best_result_from_participant_id(
                participant.number
            )

            print(participant)
            for i in results:
                print(f"    {i}")
            total_time = timedelta(seconds=0)
            for i in results:
                total_time += i.time
            
            final_results.append(
                ResultParticipant(
                    participant_number=participant.number,
                    point=sum(result.result for result in results),
                    total_time=total_time,
                )
            )
            
            print(final_results[-1])
            
            
        for_time_result = sorted(
            final_results, key=lambda result: result.total_time
        )
        final_results = sorted(
            for_time_result, key=lambda result: result.point, reverse=True
        )
        return final_results

    async def _write_result_to_database(self, results: List[ResultParticipant]) -> None:
        for i in results:
            await self._result_participant_repo.create(i)

    async def get_result_by_group(
        self, group: enums.Group
    ) -> List[SuperResultParticipant]:
        results = await self._result_participant_repo.get_by_group(group=group)
        for_time_result = sorted(
            results, key=lambda result: result.total_time
        )
        final_results = sorted(for_time_result, key=lambda result: result.point, reverse=True)
        
        for i, result in enumerate(final_results):
            result.order = i + 1
            final_results[i] = result

        return final_results
