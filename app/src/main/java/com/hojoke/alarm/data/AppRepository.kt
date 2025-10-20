package com.hojoke.alarm.data

import com.hojoke.alarm.data.local.AlarmDao
import com.hojoke.alarm.data.local.AlarmEntity
import com.hojoke.alarm.data.remote.ApiService
import com.hojoke.alarm.di.IoDispatcher
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.withContext
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AppRepository @Inject constructor(
    private val api: ApiService,
    private val alarmDao: AlarmDao,
    @IoDispatcher private val io: CoroutineDispatcher,
) {
    fun observeAlarms() = alarmDao.observeAlarms()

    suspend fun addAlarm(entity: AlarmEntity) = withContext(io) {
        alarmDao.upsert(entity)
    }

    suspend fun ping() = withContext(io) {
        runCatching { api.health() }.isSuccess
    }
}
