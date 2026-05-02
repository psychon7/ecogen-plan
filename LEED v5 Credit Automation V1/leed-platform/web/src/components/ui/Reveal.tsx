"use client";

import * as React from "react";
import { motion, useReducedMotion, type Variants } from "framer-motion";
import { cn } from "@/lib/cn";

interface RevealProps extends React.HTMLAttributes<HTMLDivElement> {
  delay?: number;
  y?: number;
  as?: "div" | "section" | "article" | "header" | "footer";
}

/**
 * Calm, glass-settling reveal animation.
 * Animates only transform + opacity + filter for GPU safety.
 */
export function Reveal({
  delay = 0,
  y = 24,
  as = "div",
  className,
  children,
  ...rest
}: RevealProps) {
  const prefersReducedMotion = useReducedMotion();

  const variants: Variants = {
    hidden: { opacity: 0, y, filter: "blur(8px)" },
    show: {
      opacity: 1,
      y: 0,
      filter: "blur(0px)",
      transition: {
        duration: 0.85,
        delay,
        ease: [0.16, 1, 0.3, 1],
      },
    },
  };

  if (prefersReducedMotion) {
    const Tag = as as React.ElementType;
    return (
      <Tag className={cn(className)} {...(rest as Record<string, unknown>)}>
        {children}
      </Tag>
    );
  }

  const MotionTag = motion[as] as React.ElementType;

  return (
    <MotionTag
      className={cn(className)}
      initial="hidden"
      whileInView="show"
      viewport={{ once: true, margin: "-80px" }}
      variants={variants}
      {...rest}
    >
      {children}
    </MotionTag>
  );
}

/**
 * Stagger child Reveal animations gently.
 */
export function RevealStagger({
  className,
  children,
  step = 0.08,
}: {
  className?: string;
  children: React.ReactNode;
  step?: number;
}) {
  const prefersReducedMotion = useReducedMotion();
  if (prefersReducedMotion) return <div className={cn(className)}>{children}</div>;
  return (
    <motion.div
      className={cn(className)}
      initial="hidden"
      whileInView="show"
      viewport={{ once: true, margin: "-80px" }}
      variants={{ show: { transition: { staggerChildren: step } } }}
    >
      {children}
    </motion.div>
  );
}
