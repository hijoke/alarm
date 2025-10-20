package com.hojoke.alarm.data.remote

import retrofit2.http.GET

interface ApiService {
    @GET("health")
    suspend fun health(): String
}
