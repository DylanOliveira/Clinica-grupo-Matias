package br.edu.clinica.repository;

import br.edu.clinica.model.Procedimento;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProcedimentoRepository extends JpaRepository<Procedimento, Long> {
    boolean existsByNome(String nome);
}

