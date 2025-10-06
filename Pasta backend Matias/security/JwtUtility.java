package com.tdebackend.clinicatde.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jws;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import org.springframework.stereotype.Component;

import java.security.Key;
import java.util.Date;
import java.util.List;

@Component
public class JwtUtility {
    private static final Key key = Keys.hmacShaKeyFor("uma-chave-secreta-muito-grande-para-jwt-256bits".getBytes());
    private static final long expirationMS = 1000 * 60 * 60; // 1 hora

    public static String generateToken(String username, List<String> role){
        return Jwts.builder()
                .setSubject(username)
                .claim("role", role)
                .setExpiration(new Date(System.currentTimeMillis() + expirationMS))
                .signWith(key, SignatureAlgorithm.HS256)
                .compact();
    }

    public static Jws<Claims> validateToken(String token){
        return Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token);
    }
}
